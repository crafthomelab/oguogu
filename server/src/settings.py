from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """환경 변수 목록들 """
    DB_HOST: str = Field(
        default="oguogu-database",
        description="db host name",
    )
    
    DB_PORT: int = Field(
        default=5432,
        description="db port number",
    )

    DB_NAME: str = Field(
        default="oguogu",
        description="디비 스키마 이름"
    )

    DB_USER: str = Field(
        default="admin",
        description="디비 유저 이름"
    )

    DB_PASSWORD: str = Field(
        default="admin123",
        description="디비 패스워드 이름"
    )
    
    S3_URL: str = Field(
        default="http://localhost:9000",
        description="s3 url",
    )
    
    S3_ACCESS_KEY: str = Field(
        default="admin",
        description="s3 access key",
    )
    
    S3_SECRET_KEY: str = Field(
        default="admin123",
        description="s3 secret key",
    )
    
    S3_BUCKET_NAME: str = Field(
        default="oguogu",
        description="s3 bucket name",
    )
    
    WEB3_PROVIDER_URL: str = Field(
        default="http://localhost:8545",
        description="web3 provider url",
    )
    
    OPERATOR_PRIVATE_KEY: str = Field(
        default="0x0000000000000000000000000000000000000000000000000000000000000000",
        description="operator private key",
    )
    
    OGUOGU_ADDRESS: str = Field(
        default="0x0000000000000000000000000000000000000000",
        description="oguogu contract address",
    )
    
    OPENAI_API_KEY: str = Field(
        default="sk-proj-****",
        description="openai api key",
    )
    
    OPENAI_MODEL_NAME: str = Field(
        default="gpt-4o",
        description="openai model name",
    )
    
    OPENAI_MODEL_TEMPERATURE: float = Field(
        default=0.0,
        description="openai model temperature",
    )