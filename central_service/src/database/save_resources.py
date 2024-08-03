from typing import List
from .MongoDbClient import MongoDbClient
from src.entities.file.File import File


def save_file(database_client: MongoDbClient, file: dict, collection_name):
    """
    Saves a file to the database.
    """
    database_client.save(file['file_id'], file, collection_name)