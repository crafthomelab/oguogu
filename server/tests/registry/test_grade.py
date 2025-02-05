from datetime import datetime, timedelta
from unittest.mock import MagicMock
from eth_account import Account
import pytest

import pytz
from src.domains import Challenge, ChallengeActivity, ChallengeType
from src.registry.challenge import ChallengeRegistryService
from src.registry.grader import ActivityGraderResponse
from src.registry.activity import ActivityRegistryService
from src.registry.transaction import TransactionManager
from src.utils import calculate_challenge_hash
from web3 import Web3

class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)

@pytest.fixture(scope='session')
def mock_proof_registry_service(activity_registry_service: ActivityRegistryService) -> ActivityRegistryService:
    activity_registry_service.grader.grade_activity = AsyncMock(return_value=ActivityGraderResponse(
        is_correct=True,
        message="Good job!"
    ))
    return activity_registry_service


@pytest.mark.asyncio(loop_scope="session")
async def test_calculate_challenge_hash(
    web3: Web3,
    user0_account: Account,
    transaction_manager: TransactionManager,
):
    nonce = 1
    reward_amount = Web3.to_wei(1, 'ether')
    challenger = user0_account.address
    title = "Test Challenge"
    challenge_type = ChallengeType.photos
    challenge_type_index = 0
    start_date = datetime.now(pytz.utc)
    end_date = datetime.now(pytz.utc) + timedelta(days=1)
    minimum_activity_count = 1
    
    challenge_hash = calculate_challenge_hash(
        title=title,
        reward=reward_amount,
        challenge_type=challenge_type,        
        challenger=challenger,
        start_date=start_date,
        end_date=end_date,
        nonce=nonce,
        minimum_activity_count=minimum_activity_count,
    )
    
    result = transaction_manager.oguogu_contract().functions.calculateChallengeHash(
        title,
        reward_amount,
        challenge_type_index,
        challenger,
        int(start_date.timestamp()),
        int(end_date.timestamp()),
        nonce,
        minimum_activity_count,
    ).call()
    result = Web3.to_hex(result)
    
    assert challenge_hash == result
    
@pytest.mark.asyncio(loop_scope="session")
async def test_calculate_challenge_hash_2(
    web3: Web3,
    user0_account: Account,
    transaction_manager: TransactionManager,
):
    nonce = 1231
    reward_amount = Web3.to_wei(1, 'ether')
    challenger = user0_account.address
    title = "Test Chal1212312lenge"
    challenge_type = ChallengeType.photos
    challenge_type_index = 0
    start_date = datetime.now(pytz.utc)
    end_date = datetime.now(pytz.utc) + timedelta(days=2)
    minimum_activity_count = 5
    
    challenge_hash = calculate_challenge_hash(
        title=title,
        reward=reward_amount,
        challenge_type=challenge_type,        
        challenger=challenger,
        start_date=start_date,
        end_date=end_date,
        nonce=nonce,
        minimum_activity_count=minimum_activity_count,
    )
    
    result = transaction_manager.oguogu_contract().functions.calculateChallengeHash(
        title,
        reward_amount,
        challenge_type_index,
        challenger,
        int(start_date.timestamp()),
        int(end_date.timestamp()),
        nonce,
        minimum_activity_count,
    ).call()
    result = Web3.to_hex(result)
    
    assert challenge_hash == result    
    


@pytest.mark.asyncio(loop_scope="session")
async def test_submit_proof(
    challenge_registry_service: ChallengeRegistryService,
    mock_proof_registry_service: ActivityRegistryService,
    transaction_manager: TransactionManager,
    user0_account: Account,
    given_user_usdt,
):
    # 1. oguogu contract에 USDT 토큰 deposit하기
    func = transaction_manager.oguogu_contract().functions.depositReward(user0_account.address, Web3.to_wei(10, 'ether'))
    await transaction_manager.asend_transaction(func, user0_account)
    
    # 2. 챌린지 정의하기
    given_challenge = Challenge.new(
        nonce=2,
        challenger_address=user0_account.address,
        reward_amount=Web3.to_wei(1, 'ether'),
        title="Test Challenge",
        type='photos',
        start_date=datetime.now(pytz.utc),
        end_date=datetime.now(pytz.utc) + timedelta(days=1),
        minimum_activity_count=1,
    )
    
    # 3. 챌린지 서명하기
    challenge_signature = await challenge_registry_service.sign_new_challenge(given_challenge)
    
    # 4. 챌린지와 함께 블록체인에 저장하기
    func = transaction_manager.oguogu_contract().functions.createChallenge(
            title=given_challenge.title,
            reward=given_challenge.reward_amount,
            challengeType=given_challenge.type.value,
            challengeSignature=challenge_signature.signature,
            startDate=int(given_challenge.start_date.timestamp()),
            endDate=int(given_challenge.end_date.timestamp()),
            nonce=given_challenge.nonce,
            minimumActivityCount=given_challenge.minimum_activity_count,
    )
    txreceipt = await transaction_manager.asend_transaction(func, user0_account)
    
    # 5. 챌린지를 서버에 등록하기
    await challenge_registry_service.register_challenge(txreceipt.transactionHash.hex())
    
    # 6. 챌린지를 조회하기
    output_challenge = await challenge_registry_service.get_challenge(given_challenge.hash)
    
    # 7. 유저가 챌린지 증명하기
    activity_content = {
        "content_type": "image/jpeg",
        "image": "test",
        'image_bytes': b'test'
    }    
    activity = ChallengeActivity.new(activity_content)
    activity_signature = transaction_manager.create_signature(activity.activity_hash, user0_account).to_0x_hex()

    # 8. 챌린지 증명 검증하기
    await mock_proof_registry_service.register_activity(challenge=output_challenge, content=activity_content)
    
    # 9. 챌린지 증명 제출하기
    await mock_proof_registry_service.submit_activity(
        challenge=output_challenge,
        activity_hash=activity.activity_hash,
        activity_signature=activity_signature
    )
    
    
    
    
    