import pytest
from eth_account import Account

from src.database.repository import ChallengeRepository
from src.registry.challenge import ChallengeRegistryService
from src.utils import send_transaction
from web3 import Web3
from web3.contract import Contract
import os
import json

from src.database.container import DataBaseContainer
from src.database.database import SessionManager
from src.database.entity import Base
from src.settings import Settings

from testcontainers.postgres import PostgresContainer
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs



@pytest.fixture(scope="session")
def oguogu_operator_private_key() -> str:
    return '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'

@pytest.fixture(scope="session")
def user0_private_key() -> str:
    return '0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d'

@pytest.fixture(scope="session")
def user1_private_key() -> str:
    return '0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a'

@pytest.fixture(scope="session")
def oguogu_operator(oguogu_operator_private_key: str) -> Account:
    return Account.from_key(
        oguogu_operator_private_key
    )

@pytest.fixture(scope="session")
def user0_account(user0_private_key) -> Account:
    return Account.from_key(user0_private_key)
    
@pytest.fixture(scope="session")
def user1_account(user1_private_key: str) -> Account:
    return Account.from_key(user1_private_key)

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15.1") as postgres:
        yield postgres
        
@pytest.fixture(scope="session")
def anvil_container():
    container = DockerContainer("craftsangjae/anvil:latest")
    container.with_exposed_ports(8545)
    
    container.start()
    try:
        wait_for_logs(container, "Listening on 0.0.0.0:8545")
        yield container
    finally:
        container.stop()


@pytest.fixture(scope="session")
def web3(anvil_container: DockerContainer):
    url = f"http://{anvil_container.get_container_host_ip()}:{anvil_container.get_exposed_port(8545)}"
    print("web3 provider url: ", url)
    return Web3(Web3.HTTPProvider(url))


@pytest.fixture(scope="session")
def test_usdt_contract(
    web3:Web3,
    oguogu_operator: Account,
) -> Contract:
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src/abis/TestUSDT.json"), "r") as f:
        abi = json.load(f)
    contract = web3.eth.contract(abi=abi['abi'], bytecode=abi['bytecode']['object'])
    
    transaction = contract.constructor().build_transaction({
        'from': oguogu_operator.address,
        'nonce': web3.eth.get_transaction_count(oguogu_operator.address),
        'gas': 2000000,
        'gasPrice': Web3.to_wei('50', 'gwei')
    })
    signed_txn = oguogu_operator.sign_transaction(transaction)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    return web3.eth.contract(abi=abi['abi'], address=tx_receipt.contractAddress)
    

@pytest.fixture
def given_user_usdt(
    test_usdt_contract: Contract, 
    oguogu_contract: Contract,
    user0_account: Account, 
    user1_account: Account,
    web3:Web3
):
    for user in [user0_account, user1_account]:
        send_transaction(
            web3, user, 
            test_usdt_contract.functions.mint(
                user.address, Web3.to_wei(1000, 'ether')
            )
        )
        
        send_transaction(
            web3, user, 
            test_usdt_contract.functions.approve(
                oguogu_contract.address,  Web3.to_wei(1000, 'ether')
            )
        )
    
    yield 
    
    for user in [user0_account, user1_account]:
        balance = test_usdt_contract.functions.balanceOf(user.address).call()
        send_transaction(
            web3, user, 
            test_usdt_contract.functions.burn(
                user.address, balance
            )
        )


@pytest.fixture(scope="session")
def oguogu_contract(
    web3:Web3,
    oguogu_operator: Account,
    test_usdt_contract: Contract,
) -> Contract:
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src/abis/OGUOGU.json"), "r") as f:
        abi = json.load(f)
    contract = web3.eth.contract(abi=abi['abi'], bytecode=abi['bytecode']['object'])
    
    # 컨트랙트 배포 트랜잭션 생성
    tx_receipt = send_transaction(web3, oguogu_operator,  contract.constructor())
    contract_address = tx_receipt.contractAddress
    
    # 컨트랙트 초기화 트랜잭션 생성
    deployed_contract = web3.eth.contract(address=contract_address, abi=abi['abi'])
    initialize_txn = deployed_contract.functions.initialize(
        _rewardToken=test_usdt_contract.address,
        _operator=oguogu_operator.address
    )
    send_transaction(web3, oguogu_operator, initialize_txn)
    return deployed_contract


@pytest.fixture(scope="session")
def local_settings(
    postgres_container: PostgresContainer, 
    anvil_container: DockerContainer,
    oguogu_operator_private_key: str,
    oguogu_contract: Contract
):
    return Settings(
        DB_HOST=postgres_container.get_container_host_ip(),
        DB_PORT=postgres_container.get_exposed_port(5432),
        DB_NAME=postgres_container.dbname,
        DB_USER=postgres_container.username,
        DB_PASSWORD=postgres_container.password,
        WEB3_PROVIDER_URL=f"http://{anvil_container.get_container_host_ip()}:{anvil_container.get_exposed_port(8545)}",
        OPERATOR_PRIVATE_KEY=oguogu_operator_private_key,
        OGUOGU_ADDRESS=oguogu_contract.address,
    )


@pytest.fixture(scope='session')
async def local_session_manager(local_settings: Settings):
    session_manager = SessionManager(settings=local_settings)

    async with session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield session_manager

    async with session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)


    
@pytest.fixture(scope='session')
async def local_database_container(local_session_manager: SessionManager):
    container = DataBaseContainer(settings=local_settings)
    container.session_manager.override(local_session_manager)
    yield container


@pytest.fixture(scope='session')
def challenge_repository(local_session_manager):
    return ChallengeRepository(session_factory=local_session_manager.session)


@pytest.fixture(scope='session')
def challenge_registry_service(challenge_repository: ChallengeRepository, local_settings: Settings):
    return ChallengeRegistryService(challenge_repository, local_settings)