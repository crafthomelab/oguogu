from datetime import datetime, timedelta
from unittest.mock import MagicMock
from eth_account import Account
import pytest

import pytz
from src.domains import Challenge
from src.registry.challenge import ChallengeRegistryService
from src.registry.grader import ProofGraderResponse
from src.registry.proof import ProofRegistryService
from src.registry.transaction import TransactionManager
from web3 import Web3

class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)

@pytest.fixture(scope='session')
def mock_proof_registry_service(proof_registry_service: ProofRegistryService) -> ProofRegistryService:
    proof_registry_service.grader.grade_proof = AsyncMock(return_value=ProofGraderResponse(
        is_correct=True,
        message="Good job!"
    ))
    return proof_registry_service


@pytest.mark.asyncio(loop_scope="session")
async def test_submit_proof(
    challenge_registry_service: ChallengeRegistryService,
    mock_proof_registry_service: ProofRegistryService,
    transaction_manager: TransactionManager,
    user0_account: Account,
    given_user_usdt,
):
    # 1. oguogu contract에 USDT 토큰 deposit하기
    func = transaction_manager.oguogu_contract().functions.depositReward(user0_account.address, Web3.to_wei(10, 'ether'))
    await transaction_manager.asend_transaction(func, user0_account)
    
    # 2. 챌린지 정의하기
    given_challenge = Challenge.new(
        challenger_address=user0_account.address,
        reward_amount=Web3.to_wei(1, 'ether'),
        title="Test Challenge",
        type="photos",
        start_date=datetime.now(pytz.utc),
        end_date=datetime.now(pytz.utc) + timedelta(days=1),
        minimum_proof_count=1,
    )
    
    # 3. 챌린지 서명하기
    challenge_signature = await challenge_registry_service.sign_new_challenge(given_challenge)
    
    # 4. 챌린지와 함께 블록체인에 저장하기
    func = transaction_manager.oguogu_contract().functions.createChallenge(
        reward=given_challenge.reward_amount,
        challengeHash=given_challenge.hash,
        challengeSignature=challenge_signature.signature,
        startDate=int(given_challenge.start_date.timestamp()),
        endDate=int(given_challenge.end_date.timestamp()),
        minimumProofCount=given_challenge.minimum_proof_count,
    )
    txreceipt = await transaction_manager.asend_transaction(func, user0_account)
    
    # 5. 챌린지를 서버에 등록하기
    await challenge_registry_service.register_challenge(txreceipt.transactionHash.hex())
    
    # 6. 챌린지를 조회하기
    output_challenge = await challenge_registry_service.get_challenge(given_challenge.hash)
    
    # 7. 유저가 챌린지 증명하기
    proof_content = {
        "content_type": "image/jpeg",
        "image_bytes": "test"
    }    
    proof_hash = mock_proof_registry_service.calculate_proof_hash(proof_content)
    proof_signature = transaction_manager.create_signature(proof_hash, user0_account).to_0x_hex()

    # 8. 챌린지 증명 검증하기
    await mock_proof_registry_service.verify_proof(
        challenge=output_challenge,
        proof_content=proof_content,
        proof_signature=proof_signature
    )
    
    # 9. 챌린지 증명 제출하기
    await mock_proof_registry_service.submit_proof(
        challenge=output_challenge,
        proof_content=proof_content,
        proof_signature=proof_signature
    )
    
    
    
    
    