from datetime import datetime, timedelta
from eth_account import Account
import pytest
import pytz
from src.database.repository import ChallengeRepository
from src.domains import Challenge, ChallengeProof, ChallengeStatus


@pytest.mark.asyncio(loop_scope="session")
async def test_create_challenge(challenge_repository: ChallengeRepository, user0_account: Account):
    challenge = Challenge.new(
        challenger_address=user0_account.address,
        reward_amount=100,
        title="test",
        type="photos",
        description="test",
        end_date=datetime.now(pytz.utc) + timedelta(days=1),
        minimum_proof_count=1,
        receipent_address=user0_account.address,
    )
    
    await challenge_repository.create_challenge(challenge)
    
    challenge = await challenge_repository.get_challenge(challenge.hash)
    assert challenge is not None
    assert challenge.hash == challenge.hash
    assert challenge.status == challenge.status
    assert challenge.challenger_address == challenge.challenger_address
    assert challenge.reward_amount == challenge.reward_amount
    assert challenge.title == challenge.title
    assert challenge.type == challenge.type
    assert challenge.description == challenge.description
    assert challenge.end_date == challenge.end_date
    assert challenge.minimum_proof_count == challenge.minimum_proof_count
    assert challenge.receipent_address == challenge.receipent_address
    

@pytest.mark.asyncio(loop_scope="session")
async def test_submit_proofs(challenge_repository: ChallengeRepository, user0_account: Account):
    challenge = Challenge.new(
        challenger_address=user0_account.address,
        reward_amount=100,
        title="test",
        type="photos",
        description="test",
        end_date=datetime.now(pytz.utc) + timedelta(days=1),
        minimum_proof_count=2,
        receipent_address=user0_account.address,
    )
    
    await challenge_repository.create_challenge(challenge)
    challenge.open(1, user0_account.address)
    
    await challenge_repository.open_challenge(challenge)
    
    proof0 = ChallengeProof.new({"test": "test0"}, datetime.now(pytz.utc))
    proof1 = ChallengeProof.new({"test": "test1"}, datetime.now(pytz.utc))
    
    await challenge_repository.add_proof(challenge.hash, proof0)
    await challenge_repository.add_proof(challenge.hash, proof1)
    
    challenge = await challenge_repository.get_challenge(challenge.hash)
    assert len(challenge.proofs) == 2
    
    challenge.success("0x1234567890")
    await challenge_repository.complete_challenge(challenge)
    
    challenge = await challenge_repository.get_challenge(challenge.hash)
    assert challenge.status == ChallengeStatus.SUCCESS
    
