from datetime import datetime, timedelta
from eth_account import Account
import pytest
import pytz
from src.database.repository import ChallengeRepository
from src.domains import Challenge, ChallengeActivity, ChallengeStatus


@pytest.mark.asyncio(loop_scope="session")
async def test_create_challenge(challenge_repository: ChallengeRepository, user0_account: Account):
    challenge = Challenge.new(
        nonce=1,
        challenger_address=user0_account.address,
        reward_amount=100,
        title="test",
        type="photos",
        start_date=datetime.now(pytz.utc),
        end_date=datetime.now(pytz.utc) + timedelta(days=1),
        minimum_activity_count=1,
    )
    
    await challenge_repository.create_challenge(challenge)
    
    result = await challenge_repository.get_challenge(challenge.hash)
    assert result is not None
    assert result.hash == challenge.hash
    assert result.status == challenge.status
    assert result.challenger_address == challenge.challenger_address
    assert result.reward_amount == challenge.reward_amount
    assert result.title == challenge.title
    assert result.type == challenge.type
    assert result.end_date == challenge.end_date
    assert result.minimum_activity_count == challenge.minimum_activity_count
    

@pytest.mark.asyncio(loop_scope="session")
async def test_submit_proofs(challenge_repository: ChallengeRepository, user0_account: Account):
    challenge = Challenge.new(
        nonce=1,
        challenger_address=user0_account.address,
        reward_amount=100,
        title="test",
        type="photos",
        start_date=datetime.now(pytz.utc),
        end_date=datetime.now(pytz.utc) + timedelta(days=1),
        minimum_activity_count=2,
    )
    
    await challenge_repository.create_challenge(challenge)
    challenge.open(1, user0_account.address)
    
    await challenge_repository.open_challenge(challenge)
    
    activity0 = ChallengeActivity.new({"test": "test0"})
    activity1 = ChallengeActivity.new({"test": "test1"})
    
    await challenge_repository.add_activity(challenge.hash, activity0)
    await challenge_repository.add_activity(challenge.hash, activity1)
    
    challenge = await challenge_repository.get_challenge(challenge.hash)
    assert len(challenge.activities) == 2
    
    challenge.success("0x1234567890", 10000)
    await challenge_repository.complete_challenge(challenge)
    
    challenge = await challenge_repository.get_challenge(challenge.hash)
    assert challenge.status == ChallengeStatus.SUCCESS
    
