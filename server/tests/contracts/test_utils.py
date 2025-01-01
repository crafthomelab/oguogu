

from eth_account import Account

from src.contracts.utils import create_hash, create_signature, verify_hash, verify_signature


def test_create_and_verify_hash(user0_account: Account):
    challenge_data = {
        "title": "아침 달리기",
        "description": "러닝 앱 화면을 찍어서 제출한다",
        "reward": 1000000000000000000,
        "deadline": 1727836800,
    }
    
    hash = create_hash(**challenge_data)
    assert verify_hash(challenge_data, hash)
    
def test_create_and_verify_signature(user0_account: Account):
    challenge_data = {
        "title": "아침 달리기",
        "description": "러닝 앱 화면을 찍어서 제출한다",
        "reward": 1000000000000000000,
        "deadline": 1727836800,
    }

    hash = create_hash(**challenge_data)
    signature = create_signature(user0_account, hash)
    assert verify_signature(user0_account.address, signature, hash)
