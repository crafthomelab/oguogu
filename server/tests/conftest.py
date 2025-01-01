import pytest
from eth_account import Account

from src.database.container import DataBaseContainer
from src.database.entity import Base
from src.settings import Settings

from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def oguogu_mnemonic():
    return "test test test test test test test test test test test junk"


@pytest.fixture(scope="session")
def oguogu_operator(oguogu_mnemonic: str) -> Account:
    return Account.from_key(
        '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'
    )


@pytest.fixture(scope="session")
def user0_account(oguogu_mnemonic: str) -> Account:
    return Account.from_key(
        '0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d'
    )

    
@pytest.fixture(scope="session")
def user1_account(oguogu_mnemonic: str) -> Account:
    return Account.from_key(
        '0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a'
    )


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15.1") as postgres:
        yield postgres
    
@pytest.fixture(scope="session")
def local_settings(postgres_container: PostgresContainer):
    return Settings(
        DB_HOST=postgres_container.get_container_host_ip(),
        DB_PORT=postgres_container.get_exposed_port(5432),
        DB_NAME=postgres_container.dbname,
        DB_USER=postgres_container.username,
        DB_PASSWORD=postgres_container.password
    )
    
@pytest.fixture(scope="session")
async def local_database_container(local_settings: Settings):
    container = DataBaseContainer(settings=local_settings)
    session_manager = container.session_manager()

    async with session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield container

    async with session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
