from .MongoDbClient import MongoDbClient
import uuid
import time

class Logger:
    """
    Class used to log the behaviour of the client.
    """

    def __init__(self, db_client: MongoDbClient, log_collection_name: str, user_id: str) -> None:
        """
        Initialized a database logger.
        """
        self.db_client = db_client
        self.log_collection_name = log_collection_name
        self.user_id = user_id

    def _generate_unique_id(self):
        """
        Generate a unique id.
        """
        return str(uuid.uuid4())
    
    def log(self, log_msg: str, file_id: str):
        """
        Saves a dictionary log to the database.
        """
        log_dict = {
            'timestamp': time.time(),
            'user_id': self.user_id,
            'file_id': file_id,
            'log_msg': log_msg
        }

        self.db_client.save(self._generate_unique_id(), log_dict, self.log_collection_name)