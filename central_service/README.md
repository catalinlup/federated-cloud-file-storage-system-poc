# Central (Backend) Service

The purpose of this service is to act a source of truth for the entire system, managing the remote file metadata database as well as the cloud storage on which the file contents are saved. The service exposes a REST API that is used to upload, download, share, modify and list accesible files. On top of this, the service communicates with a RabbitMQ broker over the AMPQ protocol. The RabbitMQ broker is used to dispatch file synchronization events to connected clients.

This service is implemented using a hexagonal architecture, heavily relying on dependency injection.

## Dependencies

The following dependencies are necessary to run this service

* **Google Cloud** - this service was designed to run in Google Cloud and rely on Google Cloud Storage. Hence, a Google Cloud Storage Bucket needs to be configured (https://cloud.google.com/storage)

* **MongoDB** - the service relies on MongoDB to store file metadata and logs. Thus, a MongoDB needs to be deployed (https://www.mongodb.com/atlas/database)

* **RabbitMQ** - the service pushes events to a RabbitMQ broker. Thus, make sure to deploy such a broker before running the service (https://www.cloudamqp.com/)

* **Docker** - we provide a Docker file that can be used to build and run the service.

* **Bash** - we provide a bash script that ca be used to deploy this service to Google Cloud.

## Configuration

The service can be configured by modifying the '.env' (or 'local.env' for local configuration) file in the 'envs' folder. The following variables need to be set:

* **LOGS_DATABASE_CONNECTION_STRING** - the connection string used to connect to the logs MondoDB database
* **LOGS_DATABASE_NAME** - the name of the MongoDB logs database
* **LOGS_COLLECTION_NAME** - the name of the logs collection
* **STORAGE_INDEX_DATABASE_CONNECTION_STRING** - the connection string used to connect to the storage index MondoDB database
* **STORAGE_INDEX_DATABASE_NAME** - the name of the MongoDB storage index database
* **STORAGE_INDEX_COLLECTION_NAME** - the name of the storage index collection
* **GOOGLE_CLOUD_BUCKET_NAME** - the name of the google cloud bucket to connect to
* **RABBIT_MQ_HOST** - the url of the RabbitMQ Host
* **RABBIT_MQ_PORT** - the RabbitMQ port
* **RABBIT_MQ_VIRTUAL_HOST** - the name of the RabbitMQ virtual host
* **RABBIT_MQ_USERNAME** - the RabbitMQ username
* **RABBIT_MQ_PASSWORD** - the RabbitMQ password

## Deployment

In order to deploy this service, please follow these steps:

- Setup a new Google Cloud Project (https://console.cloud.google.com/welcome)

- Install the gcloud CLI (https://cloud.google.com/sdk/gcloud)

- Configure Docker so that it can push images to Google Cloud (https://cloud.google.com/sdk/gcloud/reference/auth/configure-docker)

- Enable Google Cloud Artifact Registry (https://cloud.google.com/artifact-registry)

- Create a Docker Repository in the Google Cloud Artifact Registry.

- Go to 'deploy.bash' within this repository and set the *IMAGE_BASE_NAME* variable to the path of the newly created Google Cloud Artifact Registry

- Enable Google Cloud Storage and create a Google Cloud Bucket.

- Set the environment variable *GOOGLE_CLOUD_BUCKET_NAME* with the name of the newly created bucket.

- Use bash to run the *deploy.bash* script.

- Alternatively, if you want to run the service locally, run docker-compose up. Running it locally still requires you to have a Google Cloud project configured (due to the dependency of Google Cloud Storage). On top of that you need to configure and download a service key and save it as 'central_service_key.json' in the keys folder.

## Endpoints

All endpoints shoud set the following header:

**Authorization**: Basic <user_id>

### POST /central/create_file

**Request Body**: A request form containing the file to be uploded withing a field called 'uploadFile'

**Response**: The metadata of the newly created file in JSON format

### POST /central/share_file

**Request Body**:
```json
{
        "share_with": [<list of user ids to share the file with>]
}
```

**Response**: Confirmation of file sharing

### POST /central/update_file

**Request Body**: JSON encoding the list of updates to be applied to a particular file

**Request Body Example**:
```json
{
    "file_id": "4f45d67a-7a93-4629-a56f-76f4952092d2",
    "file_updates": [
        {
            "update_index": 0,
            "line_number": 0,
            "line_content": "Hello, everyone!"
        },
        {
            "update_index": 1,
            "line_number": 1,
            "line_content": "This is an incredible presentation!"
        },
        {
            "update_index": 1,
            "line_number": 10,
            "line_content": "Thanks for watching!"
        }
    ]
}
```

**Response**: The contents of the file after the update operation.

### GET /central/fetch_file_info/<file_id>

**Response**: JSON object encoding metadata about the file with the provided file id.

**Response Example**:

```json
{
    "file_content_type": "text/plain",
    "file_id": "5ee2242b-1d32-4f90-841e-e1fcce136ad2",
    "file_name": "cool.txt",
    "file_owner_id": "user123",
    "file_shared_with": [
        "user12"
    ]
}
```

### GET /central/fetch_file/<file_id>

**Response**: The contents of the file with the provided file id

### GET /central/list_files

**Resoponse**: A list of JSON objects encoding the metadata of all the files the user has access to.

**Response Example**:
```json
{
    "files": [
        {
            "file_content_type": "text/plain",
            "file_id": "02110fd2-1db5-4509-b0b8-831c69dff091",
            "file_name": "data/files/file1.txt",
            "file_owner_id": "catalin",
            "file_shared_with": []
        },
        {
            "file_content_type": "text/plain",
            "file_id": "fa6ae863-bac3-4a85-a325-e61361ebc38c",
            "file_name": "data/files/file2.txt",
            "file_owner_id": "catalin",
            "file_shared_with": []
        },
        {
            "file_content_type": "text/plain",
            "file_id": "59dbb1e3-06af-44e8-9015-c076f01b4e02",
            "file_name": "data/files/file3.txt",
            "file_owner_id": "catalin",
            "file_shared_with": [
                "user2",
                "user2"
            ]
        }
    ]
}
```