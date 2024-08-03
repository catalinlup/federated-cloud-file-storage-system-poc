from typing import List, Tuple


class StorageManager:
    """
    (Interface) / abstract class representing a storage manager.
    """

    def load_file_to_memory(self, file_id: str, return_mime_type=False):
        """
        Load file of the provided id to memory
        """
        raise Exception('Not implemented')

        

    def save_file_to_secondary_storage(self, file_id: str, content_type: str, content):
        """
        Save the provided file and content to secondary storage
        """
        raise Exception('Not implemented')
    
    def list_files(self) -> List[Tuple[str, str]]:
        """
        List all files currently stored in secondary storage.
        Returns a list of tuples, where the first item is the file id and the second item is the content type.
        """
        raise Exception('Not implemented')


