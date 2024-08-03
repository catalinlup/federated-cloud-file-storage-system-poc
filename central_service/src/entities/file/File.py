from typing import List
from .FileContent import FileContent
from .FileContentProxy import FileContentProxy
from .InMemoryFileContent import InMemoryFileContent
from src.storage.CloudStorageManager import CloudStorageManager

class File:
    """
    Encodes a file within the storage system.
    """

    def __init__(self, file_id: str, file_name: str, file_owner_id: str, file_content_type: str, file_shared_with: List[str], cloud_storage_manager: CloudStorageManager) -> None:
        """
        Initializes a file object.
        """
        self.file_id = file_id
        self.file_name = file_name
        self.file_owner_id = file_owner_id
        self.file_content_type = file_content_type
        self.file_shared_with = file_shared_with
        self.file_content = FileContentProxy(InMemoryFileContent(self.file_id, self.file_content_type, None), cloud_storage_manager)


    def get_file_content(self) -> FileContent:
        return self.file_content

    def get_content_type(self) -> str:
        return self.file_content_type

    def get_file_owner_id(self) -> str:
        return self.file_owner_id

    def get_file_name(self) -> str:
        return self.file_name

    def get_file_id(self) -> str:
        return self.file_id

    def get_file_shared_with(self) -> List[str]:
        return self.file_shared_with
    


    def to_json(self) -> dict:
        return {
            'file_id': self.file_id,
            'file_name': self.file_name,
            'file_owner_id': self.file_owner_id,
            'file_content_type': self.file_content_type,
            'file_shared_with': self.file_shared_with
        }
    

    @staticmethod
    def from_json(json_obj: dict, cloud_storage_manager: CloudStorageManager):
        return File(json_obj['file_id'], json_obj['file_name'], json_obj['file_owner_id'], json_obj['file_content_type'], json_obj['file_shared_with'], cloud_storage_manager)