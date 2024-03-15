import asyncio
import boto3
from botocore.exceptions import ClientError
import io
import S3ServiceOperator

class RealS3ServiceOperator(S3ServiceOperator):

    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, region_name: str):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    async def upload_file(self, bucket_name: str, key: str, file_stream: IO, *args, **kwargs) -> None:
        # Convert synchronous call to asynchronous
        await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: self.s3_client.upload_fileobj(file_stream, bucket_name, key)
        )

    async def download_file(self, bucket_name: str, key: str, *args, **kwargs) -> IO:
        output = io.BytesIO()
        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.s3_client.download_fileobj(bucket_name, key, output)
        )
        output.seek(0)
        return output

    async def delete_file(self, bucket_name: str, key: str, *args, **kwargs) -> None:
        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.s3_client.delete_object(Bucket=bucket_name, Key=key)
        )
