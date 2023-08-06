from uuid import UUID
from typing import List, Tuple, Mapping, NamedTuple

from anndb_api.dataset import Dataset, DatasetOpResult, SearchResultItem
from anndb_api.anndb_api_pb import core_pb2
from anndb_api.anndb_api_pb import text_dataset_pb2
from anndb_api.anndb_api_pb.text_dataset_pb2_grpc import TextDatasetStub


class TextItem(NamedTuple):
    id: UUID
    text: str
    metadata: Mapping[str,str]


class TextDataset(Dataset):

    def __init__(self, channel, rpc_metadata):
        super().__init__(TextDatasetStub(channel), rpc_metadata)

    def insert(self, text:str, metadata:Mapping[str,str] = {}) -> UUID:
        result = self.stub.Insert(text_dataset_pb2.TextDatasetRequest(
            items=[
                text_dataset_pb2.TextItem(text=text, metadata=metadata)
            ]
        ), metadata=self.rpc_metadata)
        
        return self._format_dataset_op_result_single(result)

    def insert_batch(self, items:List[TextItem]) -> List[DatasetOpResult]:
        result = self.stub.Insert(text_dataset_pb2.TextDatasetRequest(
            items=[
                text_dataset_pb2.TextItem(text=item.text, metadata=item.metadata)
                for item in items
            ]
        ), metadata=self.rpc_metadata)
        
        return self._format_dataset_op_result(result)

    def update(self, id:UUID, text:str, metadata:Mapping[str,str] = {}) -> UUID:
        result = self.stub.Update(text_dataset_pb2.TextDatasetRequest(
            items=[
                text_dataset_pb2.TextItem(
                    id=core_pb2.UUID(data=id.bytes),
                    text=text,
                    metadata=metadata
                )
            ]
        ), metadata=self.rpc_metadata)
        
        return self._format_dataset_op_result_single(result)

    def update_batch(self, items:List[TextItem]) -> List[DatasetOpResult]:
        result = self.stub.Update(text_dataset_pb2.TextDatasetRequest(
            items=[
                text_dataset_pb2.TextItem(
                    id=core_pb2.UUID(data=item.id.bytes),
                    text=item.text,
                    metadata=item.metadata
                )
                for item in items
            ]
        ), metadata=self.rpc_metadata)
        
        return self._format_dataset_op_result(result)

    def search(self, query:str, n:int) -> List[SearchResultItem]:
        result = self.stub.Search(text_dataset_pb2.TextSearchRequest(
            query=query,
            n=n
        ), metadata=self.rpc_metadata)

        return self._format_search_result(result)