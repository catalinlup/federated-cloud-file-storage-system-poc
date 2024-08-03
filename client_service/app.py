from src.storage.LocalStorageManager import LocalStorageManager
from src.pubsub.RabbitMqEventListener import RabbitMqEventListener
from src.watcher.Watcher import Watcher
from src.communication.CentralServiceProxy import CentralServiceProxy
from src.config_params import *
import sys
import os
import json
from src.client.RandomClient import RandomClient
import argparse
from src.logging.MongoDbClient import MongoDbClient
from src.logging.Logger import Logger
from threading import Thread


WATCHER_FOLDER= os.path.join(ROOT_FOLDER, 'data/watcher_folders')
BEHAVIOUR_FOLDER = os.path.join(ROOT_FOLDER, 'data/client_behaviours')

parser = argparse.ArgumentParser(
    prog='ClientServer',
    description='Spawns a client process (either a random client, a watcher)',
)

parser.add_argument('target', choices = ['watcher', 'random_client', 'experiment'])
parser.add_argument('-n', '--num', required=False, help='Number of users in the experiments')
parser.add_argument('-u', '--user', required=False, help='The user id to be used by the watcher or the random client')
parser.add_argument('-p', '--path', required=False, help='The folder path to be used by the watcher | the behaviour file path to be used by the random client.')
args = parser.parse_args()

def spawn_random_client(user, behaviour_path, share_file_users):
    """
    Spawns a random client.
    """
    behaviour_path = os.path.join(BEHAVIOUR_FOLDER, behaviour_path)
    central_service_proxy = CentralServiceProxy(CENTRAL_SERVICE_PROXY_URL, user)
    beh = json.load(open(behaviour_path, 'rb'))
    beh['share_file']['possible_users'] = share_file_users

    random_client = RandomClient(central_service_proxy, beh)

    try:
        print(f'Random client spawned (user: {user}, folder: {behaviour_path})')
        random_client.start_loop()
    except KeyboardInterrupt:
        print('Interrupted')

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

def spawn_watcher(user, folder_path):
    """
    Spawns a watcher for a certain user and folder_path
    """
    folder_path = os.path.join(WATCHER_FOLDER, folder_path)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    mongo_client = MongoDbClient(LOGS_DATABASE_CONNECTION_STRING, LOGS_DATABASE_NAME)
    logger = Logger(mongo_client, LOGS_COLLECTION_NAME, user)

    storage_manager = LocalStorageManager(folder_path, logger=logger)
    event_listener = RabbitMqEventListener(RABBIT_MQ_HOST, RABBIT_MQ_PORT, RABBIT_MQ_VIRTUAL_HOST, RABBIT_MQ_USERNAME, RABBIT_MQ_PASSWORD)
    central_service_proxy = CentralServiceProxy(CENTRAL_SERVICE_PROXY_URL, user)
    watcher = Watcher(user, storage_manager, event_listener, central_service_proxy)

    try:
        print(f'Watcher spawned (user: {user}, folder: {folder_path})')
        watcher.watch()
    except KeyboardInterrupt:
        print('Interrupted')
        watcher.close()

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


def spawn_threads(start_index, end_index, behaviour_file, share_file_users=[]):
    thread_list = []

    for i in range(start_index, end_index):
        username = f'u{i}'
        thread_watcher = Thread(target=spawn_watcher, args=(username, username))
        thread_client = Thread(target=spawn_random_client, args=(username, behaviour_file, share_file_users))

        thread_list.append(thread_watcher)
        thread_list.append(thread_client)

    return thread_list

if args.target == 'watcher':
    print(f'Spawning watcher for user {args.user} at folder path {args.path}')
    spawn_watcher(args.user, args.path)

elif args.target == 'random_client':
    print(f'Spawning random client for user {args.user} using behavior file at {args.path}')
    spawn_random_client(args.user, args.path)

elif args.target == 'experiment':
    n = int(args.num)

    total_users = [f'u{i}' for i in range(n)]
    thread_list = []
    thread_list += spawn_threads(0, n // 3, 'uploader.json', total_users)
    thread_list += spawn_threads(n // 3, 2 * n // 3, 'downloader.json', total_users)
    thread_list += spawn_threads(2 * n // 3, n, 'collaborator.json', total_users)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()