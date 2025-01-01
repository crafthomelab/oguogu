import pytest
from eth_account import Account


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
