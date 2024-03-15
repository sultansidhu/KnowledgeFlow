from abc import ABC, abstractmethod
from typing import IO


class S3ServiceOperator(ABC):

    @abstractmethod
    async def upload_file(self, bucket_name: str, key: str, file_stream: IO, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def download_file(self, bucket_name: str, key: str, *args, **kwargs) -> IO:
        pass

    @abstractmethod
    async def delete_file(self, bucket_name: str, key: str, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def get_file(self, bucket_name: str, key: str, *args, **kwargs):
        pass

