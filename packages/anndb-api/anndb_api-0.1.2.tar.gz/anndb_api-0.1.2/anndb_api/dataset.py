from typing import List, Tuple, Mapping, NamedTuple
from uuid import UUID

from anndb_api.anndb_api_pb import core_pb2


class DatasetOpResult(NamedTuple):
    id: UUID
    error: str


class SearchResultItem(NamedTuple):
    id: UUID
    metadata: Mapping[str,str]


class DatasetOpException(Exception):
    pass


class Dataset:
    
    def __init__(self, stub, rpc_metadata):
        self._stub = stub
        self._rpc_metadata = rpc_metadata

    @property
    def stub(self):
        return self._stub

    @property
    def rpc_metadata(self):
        return self._rpc_metadata

    def delete(self, id:UUID) -> UUID:
        result = self.stub.Delete(core_pb2.DeleteRequest(
            ids=[core_pb2.UUID(data=id.bytes)]
        ), metadata=self.rpc_metadata)

        return self._format_dataset_op_result_single(result)

    def delete_batch(self, ids:List[UUID]) -> List[Tuple[UUID,str]]:
        result = self.stub.Delete(core_pb2.DeleteRequest(
            ids=list(map(lambda id: core_pb2.UUID(data=id.bytes), ids))
        ), metadata=self.rpc_metadata)

        return self._format_dataset_op_result(result)

    def _format_dataset_op_result(self, result) -> List[DatasetOpResult]:
        return [
            DatasetOpResult(UUID(bytes=id.data), err.message)
            for (id, err) in zip(result.ids, result.errors)
        ]

    def _format_dataset_op_result_single(self, result) -> UUID:
        error = result.errors[0].message
        if len(error) > 0:
            raise DatasetOpException(error)

        return UUID(bytes=result.ids[0].data)

    def _format_search_result(self, result) -> List[SearchResultItem]:
        return [
            SearchResultItem(UUID(bytes=item.id), item.metadata)
            for item in result.items
        ]

