# Client Service

The purpose of this service is to emulate a Google Drive client (or clients). Since we did not implement a full Google Drive client, the service can be run in multiple modes corresponding to spawning different components of a real client:

* **watcher** - in this mode, the client simulates a watcher, which listens to file synchronization events coming from the server and manages its local storage accordingly
* **random_client** - in this mode the client simulates a user performing actions randomly, such as creating, sharing and updating files.
* **experiment** - in this mode the client spawns a certain number of random clients and associated watchers in order to simulate the use of the system at scale

## Dependencies

The following dependencies are necessary to run this service:

* **Python** - the service was implemented in Python, so you need a recent version of the Python interpreter to run it (https://www.python.org/)

* **MongoDB** - the service relies on MongoDB to store logs.

* **RabbitMQ** - the service listens to file synchronization events from a RabbitMQ broker, so such a broker needs to be setup. The central service and the client service need to use the same broker.

## Setup

* Create a Python virtual environment (https://docs.python.org/3/library/venv.html)

* Install the library dependencies using the following command:
```sh
pip install -r requirements.txt
```

## Configuration

Before running the service, the following configuration variables need to be set. The configuration variables should be set inside the *src/config_params.py* file.

Configuration variables:

* **RABBIT_MQ_HOST** - the hostname of the RabbitMQ broker
* **RABBIT_MQ_PORT** - the port of the RabbitMQ broker
* **RABBIT_MQ_VIRTUAL_HOST** - the RabbitMQ virtual host name
* **RABBIT_MQ_USERNAME** - the username of the RabbitMQ service
* **RABBIT_MQ_PASSWORD** - the password of the RabbitMQ service
* **CENTRAL_SERVICE_PROXY_URL** - the URL of the deployed central service
* **ROOT_FOLDER** - the root folder of the repository on the local machine
* **LOGS_DATABASE_CONNECTION_STRING** - connection string for the logs database
* **LOGS_DATABASE_NAME** - the name of the logs database
* **LOGS_COLLECTION_NAME** - the name of the collection of logs.

## Running the client service

### Watcher Mode

To start the client in watcher mode, run the following command:

```sh
python app.py watcher -u <the user id of the client> -p <local storage path (within the data/watcher_folders folder)>
```

### Random Client Mode

To start the service in random client mode, run the following command:

```sh
python app.py random_client -u <the user id of the client> -p <the path of the behaviour file within the data/client_behaviours folder>
```

### Experiment Mode

To start the service in experiment mode, run the following command:

```sh
python app.py experiment -n <the number of clients to spawn>
```