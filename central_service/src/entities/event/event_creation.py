from typing import List
from .Event import Event
from src.entities.FileUpdate import FileUpdate
import time
from src.utils import generate_unique_id



def _encode_file_updates(file_updates: List[FileUpdate]) -> List[dict]:
    """
    Encodes an ordered list of file updates into a list of json objects.
    """

    file_updates_jsons = []

    for i, file_update in enumerate(file_updates):
        json = dict()
        json['update_index'] = i
        json['file_update'] = file_update.to_json()
        file_updates_jsons.append(json)

    
    return file_updates_jsons

def create_file_sync_event(file_id: str, updates: List[FileUpdate], hash_before: str, hash_after: str):
    content = dict()
    content['file_id'] = file_id
    content['updates'] = _encode_file_updates(updates)
    content['hash_before'] = hash_before
    content['hash_after'] = hash_after

    return Event(generate_unique_id(), time.time(), 'file_sync', content)


def create_file_update_event(file_id: str, updates: List[FileUpdate]):

    content = dict()
    content['file_id'] = file_id
    content['updates'] = _encode_file_updates(updates)

    return Event(generate_unique_id(), time.time(), 'file_update', content)


def create_file_creation_event(file_id: str, file_content: str):
    content = dict()
    content['file_id'] = file_id
    content['file_content'] = file_content
    return Event(generate_unique_id(), time.time(), 'file_create', content)


def create_file_share_event(file_id: str):
    content = dict()
    content['file_id'] = file_id

    return Event(generate_unique_id(), time.time(), 'file_share', content)