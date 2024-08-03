from typing import List, Tuple
from src.storage.CloudStorageManager import CloudStorageManager
from  src.entities.file.InMemoryFileContent import InMemoryFileContent
from .FileContent import FileContent
import logging

class  FileContentProxy(FileContent):
    """
    Proxy for the file content
    """

    def __init__(self, file_content: InMemoryFileContent, cloud_storage_manager: CloudStorageManager) -> None:
        """
        The id of the file withing cloud storage.
        """
        super().__init__()
        self.file_content: InMemoryFileContent = file_content
        self.cloud_storage_manager: CloudStorageManager = cloud_storage_manager

    
    def _load_file_content(self):
        return self.cloud_storage_manager.download_file(self.file_content.get_file_id())
    

    def _save_file_content(self):
        self.cloud_storage_manager.upload_file(self.get_file_id(), self.get_content_type(), self.get_content())


    def apply_updates(self, updates: List[Tuple[int, str]]):
        """
        Applies a set of updates to the file content.
        """
        # copy the old content into memory
        if self.file_content.content == None:
            logging.getLogger().warn('Applying Updates - Loading content')
            self.file_content.content = self._load_file_content()
            
        
        # go through all of the updates and apply each one of them
        for update in updates:
            line_number = update[0]
            line_content = update[1]
            self.file_content.update(line_number, line_content)
        
        # save the new content to the cloud
        self._save_file_content()



        
    
    def get_file_id(self) -> str:
        """
        Returns the id of the file withing google cloud storage.
        """
        return self.file_content.get_file_id()
    
    def get_content(self) -> str:
        if self.file_content.content == None:
            logging.getLogger().warn('Getting Content -- Loading content')
            downloaded_content = self._load_file_content()
            self.file_content.content = downloaded_content
            return downloaded_content
        
        return self.file_content.get_content()
    
    def get_content_type(self) -> str:
        """
        Returns the type of the content
        """
        return self.file_content.get_content_type()
    

   