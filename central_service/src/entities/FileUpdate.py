class FileUpdate:
    """
    Object that encodes a file update
    """

    def __init__(self, line_number: int, line_content: str) -> None:
        """
        Entity representing a file update.
        """
        self.line_number = line_number
        self.line_content = line_content

    @staticmethod
    def create_from(json_obj: dict):
        return FileUpdate(json_obj['line_number'], json_obj['line_content'])
    

    def to_json(self):
        return {
            'line_number': self.line_number,
            'line_content': self.line_content
        }
    
    def to_tuple(self):
        return (self.line_number, self.line_content)

