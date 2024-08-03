from typing import List
import copy


class FileUpdate:
    """
    Encodes a file update.
    """

    def __init__(self, update_index: int, line_number: int, line_content: str) -> None:
        """
        Encodes a file update.
        """
        self.update_index = update_index
        self.line_number = line_number
        self.line_content = line_content

    
    def get_update_index(self):
        return self.update_index
    
    def get_line_number(self):
        return self.line_number
    
    def get_line_content(self):
        return self.line_content
    

    def apply(self, content: bytes) -> bytes:
        """
        Applies the current update to the old content, returning a new content.
        """
        old_content_bytes = copy.deepcopy(content)
        old_content = str(old_content_bytes, 'utf-8')
        old_content_lines = old_content.split('\n')
        old_content_num_lines = len(old_content_lines)
        new_line = self.line_content

        # edit the lines of the old content
        new_content_lines = []
        if self.line_number < len(old_content_lines):
            new_content_lines = [(line if i != self.line_number else new_line) for i, line in enumerate(old_content_lines)]
        
        else:
            new_content_lines = old_content_lines
            for i in range(old_content_num_lines, self.line_number):
                new_content_lines.append('')
            new_content_lines.append(new_line)

        
        new_content = '\n'.join(new_content_lines)
        new_content_bytes = bytes(new_content, 'utf-8')

        return new_content_bytes

    @staticmethod
    def from_json(json_obj: dict):
        return FileUpdate(json_obj['update_index'], json_obj['file_update']['line_number'], json_obj['file_update']['line_content'])
    


def parse_file_updates(updates: List[dict]) -> List[FileUpdate]:
    """
    Parses a list of json file updates into a list of file update objects.
    """
    update_list = list(map(lambda x: FileUpdate.from_json(x), updates))
    update_list = sorted(update_list, key=lambda x: x.get_update_index())

    return update_list