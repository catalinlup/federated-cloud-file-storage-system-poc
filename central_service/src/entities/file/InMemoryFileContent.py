from .FileContent import FileContent
import copy
import logging

class InMemoryFileContent(FileContent):
    """
    Object that stores the content of the file in memory.
    """

    def __init__(self, file_id: str, content_type: str, content: str) -> None:
        """
        Initializes the the in memory file content with the string encoding the content.
        """
        self.content = content
        self.content_type = content_type
        self.file_id = file_id


    def update(self, line_number: int, new_line: str):
        old_content_bytes = copy.deepcopy(self.get_content())
        old_content = str(old_content_bytes, 'utf-8')
        old_content_lines = old_content.split('\n')
        old_content_num_lines = len(old_content_lines)

        # edit the lines of the old content
        new_content_lines = []
        if line_number < len(old_content_lines):
            new_content_lines = [(line if i != line_number else new_line) for i, line in enumerate(old_content_lines)]
        
        else:
            new_content_lines = old_content_lines
            for i in range(old_content_num_lines, line_number):
                new_content_lines.append('')
            new_content_lines.append(new_line)

        
        new_content = '\n'.join(new_content_lines)
        new_content_bytes = bytes(new_content, 'utf-8')

        # save the new content
        self.content = new_content_bytes




    def get_content(self) -> str:
        """
        Returns the context of the file as a string.
        """

        if self.content == None:
            raise Exception('Content not loaded')

        return self.content
    
    def get_file_id(self) -> str:
        """
        Returns the id of the file withing google cloud storage.
        """

        return self.file_id

    def get_content_type(self) -> str:
        """
        Returns the content type of the file content
        """
        return self.content_type

    @staticmethod
    def from_json(json_obj):
        return InMemoryFileContent(json_obj['file_id'], json_obj['content_type'], json_obj['content'])