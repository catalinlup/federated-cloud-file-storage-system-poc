from typing import List
from ..entities.FileUpdate import FileUpdate
from ..entities.file.File import File
from ..pubsub.EventPublisher import EventPublisher
from .StorageController import StorageController
from ..entities.event.Event import Event
from ..entities.event.event_creation import create_file_sync_event, create_file_share_event
import logging


class SynchronizerController:
    """
    Controller used to synchronize files across clients.
    """

    def __init__(self, event_publisher: EventPublisher, storage_controller: StorageController) -> None:
        self.event_publisher: EventPublisher = event_publisher
        self.storage_controller: StorageController = storage_controller


    def perform_file_updates(self, user_id: str, file_id: str, file_updates: List[dict]) -> File:
        """
        Performs the provided file updates and returns a new file.
        Returns the file that was obtained after the updates were applied.
        """

        new_file = self._handle_update_file_event(user_id, file_id, self._parse_file_update_jsons(file_updates))

        return new_file

    


    def _parse_file_update_jsons(self, file_update_jsons: List[dict]):
        """
        Order and parse the file_update_jsons
        """

        sorted_update_jsons = sorted(file_update_jsons, key=lambda x: x['update_index'])

        file_updates = []

        for json in sorted_update_jsons:
            file_updates.append(FileUpdate.create_from(json))

        return file_updates


    def _handle_share_file_event(self, file_id: str, shared_with: List[str]):
        """
        Sends a share file event to all relevant clients whenever such an operation occures.
        """

        event = create_file_share_event(file_id)
        for user in shared_with:
            self.event_publisher.publish_event(event, user)


    
    def _handle_update_file_event(self, user_id: str, file_id: str, file_updates: List[FileUpdate]) -> File:
        """
        Handles the event of updating a file.
        """
        file: File = self.storage_controller.get_file_by_id(file_id)

        if file == None:
            raise Exception(f'File of id {file_id} does not exist')
        
        if file.get_file_owner_id() != user_id and not (user_id in file.get_file_shared_with()):
            raise Exception('Not allowed')
        

        # get the users with which the file is shared
        users = file.get_file_shared_with()
        # owner = file.get_file_owner_id()
        # users.append(owner)

   
        # get the file hash before the updates
        hash_before = file.get_file_content().get_content_hash()

        # apply the update operation
        updated_file = self.storage_controller.apply_updates_to_file(file.get_file_id(), file_updates)

        # get the hash after the file updates
        hash_after = updated_file.get_file_content().get_content_hash()


        # create a synchronization event
        sync_event = create_file_sync_event(file_id, file_updates, hash_before, hash_after)

        # send the synchronization event to all of the users

        for user in users:
            self.event_publisher.publish_event(sync_event, user)

        logging.getLogger().warn(updated_file.get_file_content().get_content())

        return updated_file

        








    
    

