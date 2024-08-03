from google.cloud import storage
import logging

class CloudStorageManager:
    """
    Object that managers cloud storage.
    Used to upload files to cloud storage and download files from cloud storage.
    """

    def __init__(self, cloud_bucket_name: str) -> None:
        self.cloud_bucket_name = cloud_bucket_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(self.cloud_bucket_name)




    def upload_file(self, file_id: str, content_type: str, content):
        """
        Uploads file to Google Cloud
        """
        blob = self.bucket.blob(file_id)
        blob.upload_from_string(content, content_type=content_type)

    def download_file(self, file_id: str):
        """
        Downloads file from google cloud storage
        """
        blob = self.bucket.blob(file_id)
        contents = blob.download_as_string()
        return contents

