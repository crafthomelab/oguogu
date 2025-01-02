from datetime import datetime, timedelta
from eth_account import Account
import pytest

import pytz
from src.domains import Challenge, ChallengeStatus
from src.registry.challenge import ChallengeRegistryService
from src.registry.proof import ProofRegistryService
from src.registry.reward import ChallengeRewardService
from src.registry.transaction import TransactionManager
from web3 import Web3
from web3.contract import Contract

@pytest.mark.asyncio(loop_scope="session")
async def test_submit_proof(
    challenge_reward_service: ChallengeRewardService,
    challenge_registry_service: ChallengeRegistryService,
    mock_proof_registry_service: ProofRegistryService,
    transaction_manager: TransactionManager,
    test_usdt_contract: Contract,
    user0_account: Account,
    user1_account: Account,
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
        description="Test Challenge Description",
        end_date=datetime.now(pytz.utc) + timedelta(days=1),
        receipent_address=user1_account.address,
        minimum_proof_count=1,
    )
    
    # 3. 챌린지 서명하기
    challenge_signature = await challenge_registry_service.sign_new_challenge(given_challenge)
    
    # 4. 챌린지와 함께 블록체인에 저장하기
    func = transaction_manager.oguogu_contract().functions.createChallenge(
        reward=given_challenge.reward_amount,
        challengeHash=given_challenge.hash,
        challengeSignature=challenge_signature.signature,
        dueDate=int(given_challenge.end_date.timestamp()),
        minimumProofCount=given_challenge.minimum_proof_count,
        receipent=given_challenge.receipent_address
    )
    txreceipt = await transaction_manager.asend_transaction(func, user0_account)
    
    # 5. 챌린지를 서버에 등록하기
    await challenge_registry_service.register_challenge(txreceipt.transactionHash.hex())
    
    # 6. 챌린지를 조회하기
    output_challenge = await challenge_registry_service.get_challenge(given_challenge.hash)
    
    # 7. 유저가 챌린지 증명하기
    proof_content = {
        "content_type": "image/jpeg",
        "image_bytes": "test2"
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
    # 10. 챌린지 완료하기
    await challenge_reward_service.complete_challenge(output_challenge.id)
    
    # 11. 챌린지 조회하기
    output_challenge = await challenge_registry_service.get_challenge(given_challenge.hash)
    
    # 12. 챌린지 완료 여부 확인하기
    assert output_challenge.status == ChallengeStatus.SUCCESS
    
    # 13. 실제로 지급되었는지 확인
    balance = test_usdt_contract.functions.balanceOf(user1_account.address).call()
    assert balance <= Web3.to_wei(1, 'ether') and balance > 0
