from flask import Flask, request, jsonify, g
from .config_params import *
from .controllers.SynchronizerController import SynchronizerController
from .controllers.StorageController import StorageController
from .pubsub.EventPublisher import EventPublisher
from .pubsub.RabbitMqPublisher import RabbitMqPublisher
from .database.MongoDbClient import MongoDbClient
from .storage.CloudStorageManager import CloudStorageManager
from .entities.event.Event import Event
from .entities.event.event_creation import create_file_sync_event
from .utils import generate_unique_id
from werkzeug.exceptions import BadRequest
from http import HTTPStatus
from flask import Response
import logging
from time import strftime
import time



app=Flask(__name__)


# setup the storage and the synchronization controller
log_client = MongoDbClient(LOGS_DATABASE_CONNECTION_STRING, LOGS_DATABASE_NAME)
storage_controller =  StorageController(CloudStorageManager(GOOGLE_CLOUD_BUCKET_NAME), MongoDbClient(STORAGE_INDEX_DATABASE_CONNECTION_STRING, STORAGE_INDEX_DATABASE_NAME), STORAGE_INDEX_COLLECTION_NAME)
event_publisher = RabbitMqPublisher(RABBIT_MQ_HOST, RABBIT_MQ_PORT, RABBIT_MQ_VIRTUAL_HOST, RABBIT_MQ_USERNAME, RABBIT_MQ_PASSWORD)
synchronization_controller = SynchronizerController(event_publisher, storage_controller)
app.config.update(
    log_client = log_client,
    event_publisher = event_publisher,
    storage_controller = storage_controller,
    synchronization_controller = synchronization_controller
)

@app.before_request
def init():
    g.log_client = app.config['log_client']
    g.event_publisher = app.config['event_publisher']
    g.storage_controller = app.config['storage_controller']
    g.synchronization_controller = app.config['synchronization_controller']
    g.request_receive_time_ms = time.time() * 1000


def get_user_id() -> str:
    """
    Fetches the id of the user from the header.
    """
    if not ('Authorization' in request.headers.keys()):
        raise BadRequest('Missing authorization header')
    authorization_header_vals = request.headers['Authorization'].split(' ')

    if len(authorization_header_vals) != 2:
        raise BadRequest('Invalid authorization header')
    
    if authorization_header_vals[0] != 'Basic':
        raise BadRequest('Invalid authorization header')
    
    return authorization_header_vals[1]



@app.route('/central/create_file', methods=['POST'])
def create_file():
    """
    Creates a file on the system.

    """
    user_id = get_user_id()

    document_data = request.files['uploadFile']
    storage_controller: StorageController = g.storage_controller
    file = storage_controller.create_file(document_data.filename, user_id,  document_data.read(), document_data.mimetype)

    return jsonify(file.to_json()), HTTPStatus.OK


@app.route('/central/share_file', methods=['POST'])
def share_file():
    """
    Shares a file with different users:
    Body:
    {
        "share_with": [<user ids>]
    }
    """
    user_id = get_user_id()
    
    body = request.json
    file_id = body['file_id']
    share_with = body['share_with']

    storage_controller: StorageController = g.storage_controller
    storage_controller.share_file(user_id, file_id, share_with)

    synchronizer: SynchronizerController = g.synchronization_controller
    synchronizer._handle_share_file_event(file_id, share_with)


    return 'File shared succesfully', HTTPStatus.OK



@app.route('/central/test_rabbit_mq', methods=['POST'])
def test_rabbit_mq():
    user_id = get_user_id()
    body = request.json
    ep: EventPublisher = g.event_publisher
    test_event = Event('test', 0, 'test', body)
    test_event_json = test_event.to_json()
    ep.publish_event(test_event, user_id)

    return jsonify(test_event_json), HTTPStatus.OK


@app.route('/central/update_file', methods=['POST'])
def update_file():
    """
    Performs content update of the file
    """
    user_id = get_user_id()
    file_id = request.json['file_id']
    file_updates = request.json['file_updates']


    synchronizer: SynchronizerController = g.synchronization_controller
    new_file = synchronizer.perform_file_updates(user_id, file_id, file_updates)
    
    return Response(new_file.get_file_content().get_content(), mimetype=new_file.get_content_type(), headers={"Content-Disposition": f"attachment;filename={new_file.get_file_name()}"})


@app.route('/central/fetch_file_info/<file_id>', methods=['GET'])
def fetch_file_info(file_id):
    """
    Fetches information about a file of the provided id.
    """

    user_id = get_user_id()
    storage_controller: StorageController = g.storage_controller

    file = storage_controller.get_file_by_id(file_id)

    
    if (user_id != file.get_file_owner_id()) and (user_id not in file.get_file_shared_with()):
        return 'Not allowed', HTTPStatus.FORBIDDEN
    
    return jsonify(file.to_json()), HTTPStatus.OK




@app.route('/central/fetch_file/<file_id>', methods=['GET'])
def fetch_file(file_id):
    """
    Fetches a file of the provided id.
    """

    user_id = get_user_id()
    storage_controller: StorageController = g.storage_controller

    file = storage_controller.get_file_by_id(file_id)

    if (user_id != file.get_file_owner_id()) and (user_id not in file.get_file_shared_with()):
        return 'Not allowed', HTTPStatus.FORBIDDEN
    
    return Response(file.get_file_content().get_content(), mimetype=file.get_content_type(), headers={"Content-Disposition": f"attachment;filename={file.get_file_name()}"})




@app.route('/central/list_files', methods=['GET'])
def list_files():
    """
    Lists all of the files the user has access to.
    """

    user_id = get_user_id()
    storage_controller: StorageController = g.storage_controller

    files = storage_controller.get_all_accesible_files(user_id)

    # only keep the files viewable to the user
    result = dict()
    result['files'] = list(map(lambda file: file.to_json(), files))

    return jsonify(result), HTTPStatus.OK



@app.after_request
def after_request(response):
    """
    Log all request response pairs.
    """
    request_end_time_ms = time.time() * 1000

    delta_time_ms = request_end_time_ms - g.request_receive_time_ms

    user_id = get_user_id()
    timestamp = time.time()
    logging.getLogger().info('%s %s %s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status, user_id, delta_time_ms)

    log_object = {
        'timestamp': timestamp,
        'remote_addr': request.remote_addr,
        'method': request.method,
        'scheme': request.scheme,
        'full_path': request.full_path,
        'response_status': response.status,
        'user_id': user_id,
        'delta_time_ms': delta_time_ms
    }
    g.log_client.save(generate_unique_id(), log_object, LOGS_COLLECTION_NAME)

    return response


@app.errorhandler(Exception)
def handle_generic_exception(e):
    """
    Handles a generic exception.
    """
    return str(e), HTTPStatus.INTERNAL_SERVER_ERROR