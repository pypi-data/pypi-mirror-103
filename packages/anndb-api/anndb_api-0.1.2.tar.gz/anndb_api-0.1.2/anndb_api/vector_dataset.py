from typing import List, Tuple, Mapping, Union, NamedTuple
from uuid import UUID

import numpy as np

from anndb_api.dataset import Dataset, DatasetOpResult, SearchResultItem
from anndb_api.anndb_api_pb import core_pb2
from anndb_api.anndb_api_pb import vector_dataset_pb2
from anndb_api.anndb_api_pb.vector_dataset_pb2_grpc import VectorDatasetStub

from anndb_api import util


class VectorItem(NamedTuple):
    id: UUID
    vector: Union[List[float], np.ndarray]
    metadata: Mapping[str,str]


class VectorDataset(Dataset):

    def __init__(self, channel, rpc_metadata):
        super().__init__(VectorDatasetStub(channel), rpc_metadata)

    def insert(self, vector:Union[List[float], np.ndarray], metadata:Mapping[str,str] = {}) -> UUID:
        result = self.stub.Insert(vector_dataset_pb2.VectorDatasetRequest(
            items=[
                vector_dataset_pb2.VectorItem(
                    vector=util.vector_proto(vector),
                    metadata=metadata
                )
            ]
        ), metadata=self.rpc_metadata)
        
        return self._format_dataset_op_result_single(result)

    def insert_batch(self, items:List[VectorItem]) -> List[DatasetOpResult]:
        result = self.stub.Insert(vector_dataset_pb2.VectorDatasetRequest(
            items=[
                vector_dataset_pb2.VectorItem(
                    vector=util.vector_proto(item.vector),
                    metadata=item.metadata
                )
                for item in items
            ]
        ), metadata=self.rpc_metadata)
        
        return self._format_dataset_op_result(result)

    def update(self, id:UUID, vector:Union[List[float], np.ndarray], metadata:Mapping[str,str] = {}) -> UUID:
        result = self.stub.Update(vector_dataset_pb2.VectorDatasetRequest(
            items=[
                vector_dataset_pb2.VectorItem(
                    id=core_pb2.UUID(data=id.bytes),
                    vector=util.vector_proto(vector),
                    metadata=metadata
                )
            ]
        ), metadata=self.rpc_metadata)
        
        return self._format_dataset_op_result_single(result)

    def update_batch(self, items:List[VectorItem]) -> List[DatasetOpResult]:
        result = self.stub.Update(vector_dataset_pb2.VectorDatasetRequest(
            items=[
                vector_dataset_pb2.VectorItem(
                    id=core_pb2.UUID(data=item.id.bytes),
                    vector=util.vector_proto(item.vector),
                    metadata=item.metadata
                )
                for item in items
            ]
        ), metadata=self.rpc_metadata)
        
        return self._format_dataset_op_result(result)

    def search(self, query:Union[List[float], np.ndarray], n:int) -> List[SearchResultItem]:
        result = self.stub.Search(vector_dataset_pb2.VectorSearchRequest(
            query=util.vector_proto(query),
            n=n
        ), metadata=self.rpc_metadata)

        return self._format_search_result(result)
