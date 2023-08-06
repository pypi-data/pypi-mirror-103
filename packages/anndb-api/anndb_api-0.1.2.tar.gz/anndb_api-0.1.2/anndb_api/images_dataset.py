from typing import List, Tuple, Mapping, Union, NamedTuple
from uuid import UUID

from PIL.Image import Image

from anndb_api.dataset import Dataset, SearchResultItem, DatasetOpResult
from anndb_api.anndb_api_pb import core_pb2
from anndb_api.anndb_api_pb import image_dataset_pb2
from anndb_api.anndb_api_pb.image_dataset_pb2_grpc import ImageDatasetStub
from anndb_api import util


class ImageItem(NamedTuple):
    id: UUID
    image: Union[Image,str]
    metadata: Mapping[str,str]


class ImagesDataset(Dataset):

    def __init__(self, channel, rpc_metadata):
        super().__init__(ImageDatasetStub(channel), rpc_metadata)

    def insert(self, image:Union[Image,str], metadata:Mapping[str,str] = {}) -> UUID:
        result = self.stub.Insert(image_dataset_pb2.ImageDatasetRequest(
            items=[
                image_dataset_pb2.ImageItem(
                    image=util.image_proto(image),
                    metadata=metadata
                )
            ]
        ), metadata=self.rpc_metadata)
        
        return self._format_dataset_op_result_single(result)

    def insert_batch(self, items:List[ImageItem]) -> List[DatasetOpResult]:
        result = self.stub.Insert(image_dataset_pb2.ImageDatasetRequest(
            items=[
                image_dataset_pb2.ImageItem(
                    image=util.image_proto(item.image),
                    metadata=item.metadata
                )
                for item in items
            ]
        ), metadata=self.rpc_metadata)
        
        return self._format_dataset_op_result(result)

    def update(self, id:UUID, image:Union[Image,str], metadata:Mapping[str,str] = {}) -> UUID:
        result = self.stub.Update(image_dataset_pb2.ImageDatasetRequest(
            items=[
                image_dataset_pb2.ImageItem(
                    id=core_pb2.UUID(data=id.bytes),
                    image=util.image_proto(image),
                    metadata=metadata
                )
            ]
        ), metadata=self.rpc_metadata)
        
        return self._format_dataset_op_result_single(result)

    def update_batch(self, items:List[ImageItem]) -> List[DatasetOpResult]:
        result = self.stub.Update(image_dataset_pb2.ImageDatasetRequest(
            items=[
                image_dataset_pb2.ImageItem(
                    id=core_pb2.UUID(data=item.id.bytes),
                    image=util.image_proto(item.image),
                    metadata=item.metadata
                )
                for item in items
            ]
        ), metadata=self.rpc_metadata)
        
        return self._format_dataset_op_result(result)

    def search_image(self, query:Union[Image,str], n:int) -> List[SearchResultItem]:
        result = self.stub.SearchImage(image_dataset_pb2.ImageSearchImageRequest(
            query=util.image_proto(query),
            n=n
        ), metadata=self.rpc_metadata)

        return self._format_search_result(result)

    def search_text(self, query:str, n:int) -> List[SearchResultItem]:
        result = self.stub.SearchText(image_dataset_pb2.ImageSearchTextRequest(
            query=query,
            n=n
        ), metadata=self.rpc_metadata)

        return self._format_search_result(result)