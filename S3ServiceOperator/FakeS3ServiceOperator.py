import S3ServiceOperator


class FakeS3ServiceOperator(S3ServiceOperator):

    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, region_name: str):
        self.aws_key_id = "Test Key ID"
        self.aws_access_key = "Test Access Key"
        self.region_name = "Test Region Name"

    async def upload_file(self, bucket_name: str, key: str, file_stream: IO, *args, **kwargs) -> None:
        print(f"Uploading file to {bucket_name} with key {key}...")

    async def download_file(self, bucket_name: str, key: str, *args, **kwargs) -> IO:
        print(f"Downloading file from {bucket_name} with key {key}")

    async def delete_file(self, bucket_name: str, key: str, *args, **kwargs) -> None:
        print(f"Deleting file {bucket_name} with key {key}")

    async def get_file(self, bucket_name: str, key: str, *args, **kwargs):
        return "Some json data"
