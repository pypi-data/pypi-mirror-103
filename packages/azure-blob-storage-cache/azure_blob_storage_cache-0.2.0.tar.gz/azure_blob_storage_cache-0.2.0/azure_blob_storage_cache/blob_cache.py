import pickle
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from .exceptions import NotCached

class BlobCache():
    def __init__(self,connection_string,container_name):
        self.connection_string = connection_string
        self.container_name = container_name

    def client(self):
        return (BlobServiceClient
                .from_connection_string(self.connection_string)
                .get_container_client(self.container_name)
            )


    def __getitem__(self,key):
        try:
            blob_client = self.client().get_blob_client(key)
            value = blob_client.download_blob().content_as_bytes()
        except ResourceNotFoundError as rnf:
            raise NotCached from rnf
        return pickle.loads(value)

    def __setitem__(self,key,value):
        blob_client = self.client().get_blob_client(key)
        blob_client.upload_blob(pickle.dumps(value))
