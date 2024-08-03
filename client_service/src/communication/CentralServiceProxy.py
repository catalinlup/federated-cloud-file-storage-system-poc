from typing import List
import requests
from urllib3 import encode_multipart_formdata

class CentralServiceProxy:
    """
    Used to make request and fetch resources from the central service
    """

    def __init__(self, url: str, user_id: str) -> None:
        self.url = url
        self.user_id = user_id

        self.paths = {
            'create_file': '/central/create_file',
            'share_file': '/central/share_file',
            'get_file_info': '/central/fetch_file_info',
            'list_files': '/central/list_files',
            'get_file': '/central/fetch_file',
            'update_file': '/central/update_file'
        }

    def _make_auth_header(self, user_id: str) -> dict:
        return {'Authorization': f'Basic {user_id}'}
    
    def _make_full_path(self, action_id: str) -> str:
        return self.url + '/' + self.paths[action_id]
    
    def update_file(self, file_id: str, updates: List[dict]):
        request_body = {
            'file_id': file_id,
            'file_updates': updates
        }

        r = requests.post(url=self._make_full_path('update_file'), json=request_body, headers=self._make_auth_header(self.user_id))
        print(r.content)
        r.raise_for_status()

        return r.content


    def create_file(self, filename: str, filepath: str, content_type: str):
        fields = {
            "uploadFile": (filename, open(filepath).read(), content_type)
        }

        encoder, header = encode_multipart_formdata(fields)
        print(encoder)
        headers = self._make_auth_header(self.user_id)
        headers['Content-Type'] = header
        r = requests.post(url=self._make_full_path('create_file'), data=encoder,  headers=headers)
        print(r.content)
        r.raise_for_status()

        return r.json()
    
    def share_file(self, file_id: str, share_with: List[str]):
        request_body = {
            'file_id': file_id,
            'share_with': share_with,
        }

        r = requests.post(url=self._make_full_path('share_file'), json=request_body, headers=self._make_auth_header(self.user_id))
        print(r.content)
        r.raise_for_status()

        return r.content
    
    def get_file_info(self, file_id):
        r = requests.get(url=self._make_full_path('get_file_info') + '/' + str(file_id), headers=self._make_auth_header(self.user_id))
        print(r.content)
        r.raise_for_status()

        return r.json()
    
    def list_files(self):
        r = requests.get(url=self._make_full_path('list_files'), headers=self._make_auth_header(self.user_id))
        r.raise_for_status()

        return r.json()
    
    def get_file(self, file_id):
        r = requests.get(url=self._make_full_path('get_file') + '/' + str(file_id), headers=self._make_auth_header(self.user_id))
        r.raise_for_status()

        return r.content
        
    

    
