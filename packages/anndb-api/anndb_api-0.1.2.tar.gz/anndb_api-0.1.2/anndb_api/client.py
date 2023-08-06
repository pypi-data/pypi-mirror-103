import grpc

from anndb_api.images_dataset import ImagesDataset
from anndb_api.text_dataset import TextDataset
from anndb_api.vector_dataset import VectorDataset


class Client:

    SERVER_ADDR = 'grpc-api.anndb.com:1433'

    def __init__(self, api_key:str):
        self._api_key = api_key
        self._channel = grpc.secure_channel(self.SERVER_ADDR, grpc.ssl_channel_credentials())

    def close(self):
        self._channel.close()

    def images(self, dataset_name:str) -> ImagesDataset:
        return ImagesDataset(self._channel, self._rpc_metadata(dataset_name))

    def text(self, dataset_name:str) -> TextDataset:
        return TextDataset(self._channel, self._rpc_metadata(dataset_name))

    def vector(self, dataset_name:str) -> VectorDataset:
        return VectorDataset(self._channel, self._rpc_metadata(dataset_name))

    def _rpc_metadata(self, dataset_name):
        return [
            ('authorization', self._api_key),
            ('dataset', dataset_name)
        ]