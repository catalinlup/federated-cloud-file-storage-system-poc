from src.storage.CloudStorageManager import CloudStorageManager
from src.database.MongoDbClient import MongoDbClient
from src.entities.file.File import File
from src.database.save_resources import *
from src.database.fetch_resources import *
from src.entities.FileUpdate import FileUpdate
from src.utils import generate_unique_id
from src.config_params import *
import logging


class StorageController:
    """
    Object responsible for controlling the storage system.
    """


    def __init__(self, cloud_storage_manager: CloudStorageManager, file_database_client: MongoDbClient, files_collection_name: str) -> None:
        """
        Initializes the storage controller.
        """
        self.cloud_storage_manager = cloud_storage_manager
        self.file_database_client = file_database_client
        self.files_collection_name = files_collection_name
    

    
    def create_file(self, file_name: str, owner_id: str, content: str = '', content_type = 'text/plain') -> File:
        file_id = generate_unique_id()
        
        # create an empty file in cloud storage
        self.cloud_storage_manager.upload_file(file_id, content_type, content)

        # create a file object
        file = File(file_id, file_name, owner_id, content_type, [], self.cloud_storage_manager)

        # save the file object in the database
        save_file(self.file_database_client, file.to_json(), self.files_collection_name)

        return file


    def file_exists(self, file_id: str) -> bool:
        """
        Returns true if a file of the given id exists, false otherwise.
        """
        return file_of_id_exists(self.file_database_client, file_id, self.files_collection_name)

    
    def get_file_by_id(self, file_id: str) -> File:
        """
        Return a file by its id.
        """
        file_json = fetch_file_by_id(self.file_database_client, file_id, self.files_collection_name)
        file = File.from_json(file_json, self.cloud_storage_manager)

        return file


    def get_all_files(self) -> List[File]:
        """
        Return all the files in the storage system.
        """
        file_jsons = fetch_all_files(self.file_database_client, self.files_collection_name)
        files = list(map(lambda x: File.from_json(x, self.cloud_storage_manager), file_jsons))
        return files
    
    def get_all_accesible_files(self, user_id: str) -> List[File]:
        """
        Returns all the accessible files from the storage system.
        """

        file_jsons = fetch_all_accesible_files(self.file_database_client, user_id, self.files_collection_name)
        files = list(map(lambda  x: File.from_json(x, self.cloud_storage_manager), file_jsons))
        return files
    
    
    
    def get_files_of_ids(self, id_set: list) -> List[File]:
        """
        Return all the files that have the following ids.
        """
        file_jsons = fetch_all_files_by_id_set(self.file_database_client, id_set, self.files_collection_name)
        files = list(map(lambda x: File.from_json(x, self.cloud_storage_manager), file_jsons))
        return files
    

    def share_file(self, user_id: str, file_id: str, new_user_ids: List[str]):
        """
        Shares a file with another user.
        """
        file = self.get_file_by_id(file_id)

        if file.file_owner_id != user_id:
            raise Exception('Not allowed')

        file.file_shared_with += new_user_ids
        # logging.getLogger().warn(file.to_json())
        save_file(self.file_database_client, file.to_json(), self.files_collection_name)
    

    def apply_updates_to_file(self, file_id: str, file_updates: List[FileUpdate]) -> File:
        """
        Applies updates to the file specified by the file id.
        """
        # convert the file updates to tuple
        file_updates_tuples = list(map(lambda f: f.to_tuple(), file_updates))

        # fetch the file to apply the updates to
        file = self.get_file_by_id(file_id)

        # apply the updates to the file
        file.get_file_content().apply_updates(file_updates_tuples)

        return file




