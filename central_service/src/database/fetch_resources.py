from typing import List
from .MongoDbClient import MongoDbClient
from src.entities.file.File import File

def fetch_all_files(database_client: MongoDbClient, collection_name: str) -> List[dict]:
    """
    Fetches all files in the database.
    """
    files_json = list(map(lambda x: x[1], database_client.get_all(collection_name)))
    return files_json


def fetch_file_by_id(database_client: MongoDbClient, file_id: str, collection_name: str) -> dict:
    """
    Fetches a file by id
    """
    files_json = list(database_client.get_all_by_attribute('file_id', file_id, collection_name))

    if len(files_json) == 0:
        return None
    
    return files_json[0]


def fetch_all_files_by_id_set(database_client: MongoDbClient, file_ids: list, collection_name: str) -> List[dict]:
    """
    Fetch the files of the following ids.
    """
    files_json = list(database_client.get_all_by_query({'file_id': {'$in': list(file_ids)}}, collection_name))

    return files_json

def fetch_all_files_by_owner_id(database_client: MongoDbClient, owner_id: list, collection_name: str) -> List[dict]:
    """
    Fetch all files of the provided owner
    """

    files_json = list(database_client.get_all_by_attribute('file_owner_id', owner_id, collection_name))

    if len(files_json) == 0:
        return None
    
    return files_json[0]


def fetch_all_accesible_files(database_client: MongoDbClient, user_id: list, collection_name: str) -> List[dict]:
    """
    Fetch all files that are accesible to the user.
    """

    query_1 = {'file_owner_id': user_id}
    query_2 = {'file_shared_with': user_id}
    query = {'$or': [query_1, query_2]}

    files_json = list(database_client.get_all_by_query(query, collection_name))

    return files_json


def file_of_id_exists(database_client: MongoDbClient, file_id: str, collection_name: str) -> bool:
    """
    Returns true if a file of the specified id exists, else return false.
    """
    return fetch_file_by_id(database_client, file_id, collection_name) != None