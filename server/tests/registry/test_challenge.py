from datetime import datetime, timedelta
from eth_account import Account
import pytest
import pytz
from src.domains import Challenge, ChallengeStatus
from src.registry.challenge import ChallengeRegistryService
from src.utils import send_transaction
from web3 import Web3
from web3.contract import Contract

@pytest.mark.asyncio(loop_scope="session")
async def test_open_challenge_scenario(
    challenge_registry_service: ChallengeRegistryService,
    web3: Web3,
    oguogu_operator: Account,
    user0_account: Account,
    oguogu_contract: Contract,
    given_user_usdt,
):
    """ 
    """
    # 1. oguogu contract에 USDT 토큰 deposit하기
    send_transaction(web3, user0_account, oguogu_contract.functions.depositReward(user0_account.address, Web3.to_wei(10, 'ether')))
    
    # 2. 챌린지 정의하기
    given_challenge = Challenge.new(
        nonce=1,
        challenger_address=user0_account.address,
        reward_amount=Web3.to_wei(1, 'ether'),
        title="Test Challenge",
        type="photos",
        start_date=datetime.now(pytz.utc),
        end_date=datetime.now(pytz.utc) + timedelta(days=1),
        minimum_activity_count=1,
    )
    
    # 3. 챌린지 서명하기
    challenge_signature = await challenge_registry_service.sign_new_challenge(given_challenge)
    
    # 4. 챌린지와 함께 블록체인에 저장하기
    txreceipt = send_transaction(
        web3, 
        user0_account, 
        oguogu_contract.functions.createChallenge(
            reward=given_challenge.reward_amount,
            challengeHash=given_challenge.hash,
            challengeSignature=challenge_signature.signature,
            startDate=int(given_challenge.start_date.timestamp()),
            endDate=int(given_challenge.end_date.timestamp()),
            minimumActivityCount=given_challenge.minimum_activity_count,
        )
    )
    
    # 5. 챌린지를 서버에 등록하기
    await challenge_registry_service.register_challenge(txreceipt.transactionHash.hex())
    
    # 6. 챌린지를 조회하기
    output_challenge = await challenge_registry_service.get_challenge(given_challenge.hash)
    assert output_challenge.status == ChallengeStatus.OPEN
