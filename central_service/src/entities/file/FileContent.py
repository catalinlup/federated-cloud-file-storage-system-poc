from src.utils import compute_hash

class FileContent:
    """
    Interface class for the content of a file.
    """


    def get_content_type(self) -> str:
        """
        Returns the type of the content
        """
        raise Exception('No implementation!')


    def get_content(self) -> str:
        """
        Returns the context of the file as a string.
        """
        raise Exception('No implementation!')
    
    def get_file_id(self) -> str:
        """
        Returns the id of the file this content belongs to.
        """

        raise Exception('No implementation!')
    

    def get_content_hash(self) -> int:
        """
        Returns the hash of the content.
        """
        content = self.get_content()
        return compute_hash(content)
    

    def to_json(self) -> dict:
        return {
            'file_id': self.get_file_id(),
            'content': self.get_content()
        }