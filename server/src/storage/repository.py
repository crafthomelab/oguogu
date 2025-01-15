from typing import Optional
from src.settings import Settings
import aioboto3
from types_aiobotocore_s3.client import S3Client
from aiobotocore.response import StreamingBody
from contextlib import asynccontextmanager

class ObjectRepository:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.endpoint_url = settings.S3_URL
        self.access_key_id = settings.S3_ACCESS_KEY
        self.secret_access_key = settings.S3_SECRET_KEY
        self.bucket_name = settings.S3_BUCKET_NAME
        self.session = aioboto3.Session()
        
    async def acreate_bucket(self):
        async with self.client() as client:
            client: S3Client
            await client.create_bucket(Bucket=self.bucket_name)
            

    async def astream_by_id(self, key: str) -> StreamingBody:
        async with self.client() as client: 
            client: S3Client
            response = await client.get_object(Bucket=self.bucket_name, Key=key)
            return response['Body']
        
    async def asave(
        self, 
        content: bytes, 
        key: str, 
        content_type: Optional[str] = None
    ):
        async with self.client() as client:
            client: S3Client
            await client.put_object(
                Bucket=self.bucket_name, 
                Key=key, 
                Body=content,
                ContentType=content_type    
            )
        
    @asynccontextmanager
    async def client(self):
        async with self.session.client(
            's3',
            region_name='ap-northeast-2',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
        ) as client:
            yield client
        