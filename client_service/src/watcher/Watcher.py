from typing import List
from ..storage.StorageManager import StorageManager
from ..pubsub.EventListener import EventListener
from ..entities.FileUpdate import FileUpdate, parse_file_updates
from ..communication.CentralServiceProxy import CentralServiceProxy
import metrohash
import copy
import json

class Watcher:
    """
    Class responsible for listening to update events and applying update events accordingly.
    """

    def __init__(self, user_id: str, storage_manager: StorageManager, event_listener: EventListener, central_service_proxy: CentralServiceProxy) -> None:
        """
        Initializes a watcher component.
        """
        self.user_id = user_id
        self.storage_manager = storage_manager
        self.event_listener = event_listener
        self.central_service_proxy = central_service_proxy


        # configure the event callback
        self.event_listener.on_event_received(user_id, lambda ch, method, properties, body: self._handle_new_event(json.loads(body)))

        # whenever the watcher is initialized, start the sync process with the server
        self._sync_all_files()


    def watch(self):
        """
        Makes the watcher start watching for events.
        """
        self.event_listener.listen()
    

    def close(self):
        self.event_listener.close()


    def _handle_new_event(self, event: dict):
        """
        Handles the arrival of a new event
        """

        print('Processed event', event)


        if event['event_type'] == "file_sync":
            self._handle_file_sync_event(event)
            return

        if event['event_type'] == 'file_share':
            self._handle_file_share_event(event)
            return
        
        print('Unrecognized event', event)

    def _compute_hash(self, x):
        return metrohash.hash64_int(x, seed=0)


    def _handle_file_share_event(self, file_share_event: dict):
        """
        Handles the event of sharing a file.
        """
        file_id = file_share_event['content']['file_id']
        self._sync_file(file_id)


    def _handle_file_sync_event(self, file_sync_event: dict):
        """
        Handles a file
        """

        file_id = file_sync_event['content']['file_id']
        updates: List[FileUpdate] = parse_file_updates(file_sync_event['content']['updates'])
        hash_before = file_sync_event['content']['hash_before']
        hash_after = file_sync_event['content']['hash_after']

        # load the file from seconday storage
        local_file_content, local_content_type = self.storage_manager.load_file_to_memory(file_id, return_mime_type=True)
        local_file_content_hash = self._compute_hash(local_file_content)

        # if the initial hashes don't match, redownload the file
        if local_file_content_hash != hash_before:
            print('Initial hash did not match. Refatching files')
            print('Local hash', local_file_content_hash)
            print('Remote hash', hash_before)
            self._sync_file(file_id)
            return
        
        # apply the updates to the file content
        new_local_file_content = self._apply_file_updates(local_file_content, updates)

        
        # compute the new hash
        new_local_file_content_hash = self._compute_hash(new_local_file_content)

        # it means that the updates were not applied correctly, so refresh
        if new_local_file_content_hash != hash_after:
            print('Final hash did not match. Refatching files')
            print('Local hash before', local_file_content_hash)
            print('Local hash after', new_local_file_content_hash)
            print('Local content', new_local_file_content)
            print('Remote hash', hash_after)
            self._sync_file(file_id)
            return
        
        # save the changes to the local file
        self.storage_manager.save_file_to_secondary_storage(file_id, local_content_type, new_local_file_content)


    def _sync_file(self, file_id: str):
        """
        Syncs a file with the centralized service by downloading it and storing it in the local file system.
        """

        file_info = self.central_service_proxy.get_file_info(file_id)
        file_content = self.central_service_proxy.get_file(file_id)
        content_type = file_info['file_content_type']
        self.storage_manager.save_file_to_secondary_storage(file_id, content_type, file_content)

    def _sync_all_files(self):
        """
        Syncs all files in the cloud storage.
        """

        file_info_list = self.central_service_proxy.list_files()
        print(file_info_list)
        file_infos = file_info_list['files']

        for file_info in file_infos:
            try:
                file_id = file_info['file_id']
                file_content_type = file_info['file_content_type']
                file_content = self.central_service_proxy.get_file(file_id)
                self.storage_manager.save_file_to_secondary_storage(file_id, file_content_type, file_content)

            except:
                continue

    def _apply_file_updates(self, content: bytes, file_updates: List[FileUpdate]):
        """
        Applies the provided file updates and returns a version of the content with the new file updates.
        """
        
        sorted_file_updates = sorted(file_updates, key=lambda x: x.get_update_index())

        # print(sorted_file_updates)

        new_content = copy.deepcopy(content)

        for file_update in sorted_file_updates:
            # print('Update')
            new_content = file_update.apply(new_content)
        
        return new_content
    

