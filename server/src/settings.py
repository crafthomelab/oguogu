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
    
    OPENAI_MODEL: str = Field(
        default="gpt-4o",
        description="openai model name",
    )