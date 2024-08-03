from typing import List
from src.communication.CentralServiceProxy import CentralServiceProxy
import random
import json
from src.config_params import *
import os
import time

class RandomClient:
    """
    Client that performs random behaviour.
    """

    def __init__(self, service_proxy: CentralServiceProxy, behavior_config: dict) -> None:
        """
        Initializes a random client
        """
        self.service_proxy = service_proxy
        self.behavior_config = behavior_config

    
    def start_loop(self):
        frequency = self.behavior_config['action_frequency_s']

        print(f'Random client loop started at frequency: {frequency}')

        while True:
            self._perform_random_action()
            time.sleep(frequency)

    def _perform_random_action(self):
        print('-----')
        possible_actions = ['create_file', 'share_file', 'update_file', 'get_file', 'get_file_info']
        associated_weights = [self.behavior_config[a]['p'] for a in possible_actions]

        # choose an action
        chosen_action = random.choices(possible_actions, associated_weights)[0]

        if chosen_action == 'create_file':
            self._perform_create_file(self.behavior_config['create_file']['possible_content'])
            return

        if chosen_action == 'share_file':
            self._perform_share_file(self.behavior_config['share_file']['possible_users'])
            return

        if chosen_action == 'update_file':
            self._perform_update_file(self.behavior_config['update_file']['possible_updates'])
            return

        if chosen_action == 'get_file':
            self._perform_get_file()
            return

        if chosen_action == 'get_file_info':
            self._perform_get_file_info()
            return

        print(f'Unrecognized action {chosen_action}')

        # print('-----')

        

    
    def _perform_create_file(self, possible_content: List[str]):
        """
        Perform a create file random action.
        """
        chosen_content = random.choice(possible_content)
        chosen_filepath = os.path.join(ROOT_FOLDER, chosen_content)
        content_type = "text/plain"
        
        print(f'create_file({chosen_content, chosen_filepath, content_type})')

        self.service_proxy.create_file(chosen_content, chosen_filepath, content_type)

    def _pick_random_file(self) -> str:
        """
        Picks a random file to perform an action on.
        Returns 'None' if no random file could be picked.
        """
        accessible_files = self.service_proxy.list_files()['files']
        if len(accessible_files) == 0:
            return None
        
        chosen_file = random.choice(accessible_files)
        chosen_file_id = chosen_file['file_id']
        return chosen_file_id


    
    def _perform_share_file(self, possible_users: List[str]):
        chosen_user = random.choice(possible_users)
        chosen_file_id = self._pick_random_file()

        if chosen_file_id == None:
            return None

        print(f'share_file({chosen_file_id}, [{chosen_user}])')

        self.service_proxy.share_file(chosen_file_id, [chosen_user])

    def _perform_update_file(self, possible_updates: List[str]):
        chosen_update_path = random.choice(possible_updates)
        chosen_update_content = json.load(open(os.path.join(ROOT_FOLDER,chosen_update_path), 'rb'))

        chosen_file_id = self._pick_random_file()

        if chosen_file_id == None:
            return None
        
        print(f'update_file({chosen_file_id}, {chosen_update_path})')
        self.service_proxy.update_file(chosen_file_id, chosen_update_content)

    
    def _perform_get_file(self):
        chosen_file_id = self._pick_random_file()

        if chosen_file_id == None:
            return None

        print(f'get_file({chosen_file_id})')
        self.service_proxy.get_file(chosen_file_id)

    
    def _perform_get_file_info(self):
        chosen_file_id = self._pick_random_file()

        if chosen_file_id == None:
            return None

        print(f'get_file_info({chosen_file_id})')
        self.service_proxy.get_file_info(chosen_file_id)

    
