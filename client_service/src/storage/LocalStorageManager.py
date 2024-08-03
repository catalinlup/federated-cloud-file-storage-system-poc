from typing import List, Tuple
from .StorageManager import StorageManager
from ..mime_type_converstion import convert_mime_type_to_file_ext, convert_file_extenstion_to_mimetype
import os
from os import walk
from ..logging.Logger import Logger


class LocalStorageManager(StorageManager):
    """
    Manages local storage.
    """

    def __init__(self, folder_path: str, logger: Logger=None) -> None:
        super().__init__()
        self.folder_path = folder_path
        self.logger = logger

    
    def _list_all_files_in_folder(self, folder_path: str):
        f = []
        for (dirpath, dirnames, filenames) in walk(folder_path):
            f.extend(filenames)
            break

        return f

    def load_file_to_memory(self, file_id: str, return_mime_type=False):
        """
        Load file of the provided id to memory
        """

        file_names = self._list_all_files_in_folder(self.folder_path)
        file_path = None

        for file_name in file_names:
            if file_id in file_name:
                file_path = file_name
        
        if file_path == None:
            raise Exception('Could not find file of file id')
        
        file = open(os.path.join(self.folder_path, file_path), 'rb')
        file_content = file.read()

        if return_mime_type:
            file_ext = file_path.split('.')[1]
            return file_content, convert_file_extenstion_to_mimetype(file_ext)

        return file_content


    def save_file_to_secondary_storage(self, file_id: str, content_type: str, content):
        """
        Save the provided file and content to secondary storage
        """
        
        file_extension = convert_mime_type_to_file_ext(content_type)
        file_name = file_id + '.' + file_extension

        full_path = os.path.join(self.folder_path, file_name)

        file = open(full_path, 'wb')
        file.write(content)

        if self.logger != None:
            try:
                self.logger.log('File saved to secondary storage', file_id)
            except:
                print('Could not save log')


    
    def list_files(self) -> List[Tuple[str, str]]:
        """
        List all files currently stored in secondary storage.
        Returns a list of tuples, where the first item is the file id and the second item is the content type.
        """
        files =  self._list_all_files_in_folder(self.folder_path)

        file_content_type_pairs = []

        for file in files:
            file_id_ext = file.split('.')
            file_id = file_id_ext[0]
            file_ext = file_id_ext[1]
            content_type = convert_file_extenstion_to_mimetype(file_ext)

            file_content_type_pairs.append((file_id, content_type))

        return file_content_type_pairs



