import os
from dotenv import load_dotenv

load_dotenv()

LOGS_DATABASE_CONNECTION_STRING=os.environ['LOGS_DATABASE_CONNECTION_STRING']
LOGS_COLLECTION_NAME=os.environ['LOGS_COLLECTION_NAME']
LOGS_DATABASE_NAME=os.environ['LOGS_DATABASE_NAME']
STORAGE_INDEX_DATABASE_CONNECTION_STRING=os.environ['STORAGE_INDEX_DATABASE_CONNECTION_STRING']
STORAGE_INDEX_COLLECTION_NAME=os.environ['STORAGE_INDEX_COLLECTION_NAME']
STORAGE_INDEX_DATABASE_NAME=os.environ['STORAGE_INDEX_DATABASE_NAME']
GOOGLE_CLOUD_BUCKET_NAME=os.environ['GOOGLE_CLOUD_BUCKET_NAME']
RABBIT_MQ_HOST=os.environ['RABBIT_MQ_HOST']
RABBIT_MQ_PORT=os.environ['RABBIT_MQ_PORT']
RABBIT_MQ_VIRTUAL_HOST=os.environ['RABBIT_MQ_VIRTUAL_HOST']
RABBIT_MQ_USERNAME=os.environ['RABBIT_MQ_USERNAME']
RABBIT_MQ_PASSWORD=os.environ['RABBIT_MQ_PASSWORD']



