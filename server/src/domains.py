from dataclasses import dataclass
from decimal import Decimal
import random
from typing import Dict, List, Literal, Optional, Union
from datetime import datetime
import pytz
from src.exceptions import ClientException
from web3 import Web3
from enum import Enum

from src.utils import calculate_challenge_hash, create_hash


@dataclass
class Challenge:
    """ Challenge 도메인 """
    hash: str
    id: Optional[int]
    nonce: int
    status: "ChallengeStatus"
    
    challenger_address: str
    reward_amount: Union[int, Decimal]
    
    title: str
    type: Literal["photos"]
    
    start_date: datetime
    end_date: datetime
    minimum_activity_count: int

    activities: List["ChallengeActivity"]
    
    payment_transaction: Optional[str] = None
    payment_reward: int = 0
    complete_date: Optional[datetime] = None
    
    @staticmethod
    def new(
        nonce: int,
        challenger_address: str,
        reward_amount: int,
        title: str,
        type: Literal["photos"],
        start_date: datetime,
        end_date: datetime,
        minimum_activity_count: int,
    ) -> "Challenge":
        if reward_amount <= 0:
            raise ClientException("Reward amount must be greater than 0")
        
        if minimum_activity_count <= 0:
            raise ClientException("Minimum activity count must be greater than 0")
        
        if type != "photos":
            raise ClientException("Invalid challenge type")
        
        if not Web3.is_address(challenger_address):
            raise ClientException("Invalid challenger address")
        challenger_address = Web3.to_checksum_address(challenger_address)
        
        challenge_hash = calculate_challenge_hash(
            title=title,
            reward=reward_amount,
            challenge_type=type,
            challenger=challenger_address,
            start_date=start_date,
            end_date=end_date,
            nonce=nonce,
            minimum_activity_count=minimum_activity_count,
        )
        
        return Challenge(
            id=None,
            nonce=nonce,
            hash=challenge_hash,
            status=ChallengeStatus.INIT,
            challenger_address=challenger_address,
            reward_amount=reward_amount,
            title=title,
            type=type,
            start_date=start_date,
            end_date=end_date,
            minimum_activity_count=minimum_activity_count,
            activities=[],
            payment_transaction=None,
            complete_date=None,
        )
        
    def available_to_submit_activity(self) -> bool:
        return (
            self.status == ChallengeStatus.OPEN
            and self.end_date >= datetime.now(pytz.utc)
            and len(self.activities) < self.minimum_activity_count
        )   
        
    def available_to_complete(self) -> bool:
        """ 챌린지 완료 처리 가능한지 여부 """
        if self.status != ChallengeStatus.OPEN:
            return False
        
        if len(self.activities) >= self.minimum_activity_count:
            return True
        
        return self.end_date < datetime.now(pytz.utc)

    def open(
        self, 
        challenge_id: int,
        challenger_address: str
    ):
        self.id = challenge_id
        self.challenger_address = Web3.to_checksum_address(challenger_address)
        self.status = ChallengeStatus.OPEN
        
    def success(self, payment_transaction: str, payment_reward:int ,complete_date: datetime=None):        
        if complete_date is None:
            complete_date = datetime.now(pytz.utc)
        self.status = ChallengeStatus.SUCCESS
        self.payment_transaction = payment_transaction
        self.payment_reward = payment_reward
        self.complete_date = complete_date
    
    def fail(self, payment_transaction: str, payment_reward:int, complete_date: datetime=None):
        if complete_date is None:
            complete_date = datetime.now(pytz.utc)
        self.status = ChallengeStatus.FAILED
        self.payment_transaction = payment_transaction
        self.payment_reward = payment_reward
        self.complete_date = complete_date
        


class ChallengeStatus(Enum):
    """ 챌린지 상태 """
    INIT = 'INIT' # challenge signature 생성된 상태
    OPEN = 'OPEN' # challenge가 Network에 등록된 상태
    SUCCESS = 'SUCCESS' # challenge가 성공한 상태
    FAILED = 'FAILED' # challenge가 실패한 상태    


@dataclass
class ChallengeActivity:
    """ 챌린지 수행 활동 """
    activity_hash: str
    
    activity_transaction: Optional[str] = None
    activity_date: Optional[datetime] = None
    
    @staticmethod
    def new(content: Dict[str, any]) -> "ChallengeActivity":
        activity_hash = create_hash(**content)
        return ChallengeActivity(
            activity_hash=activity_hash, 
            activity_transaction=None,
            activity_date=None,
        )
        
    def is_completed(self) -> bool:
        return self.activity_transaction is not None
        
    def complete(self, activity_transaction: str, activity_date: datetime):
        self.activity_transaction = activity_transaction
        self.activity_date = activity_date

@dataclass
class ChallengeSignature:
    """ 챌린지 서명 도메인 """
    challenge_hash: str
    signature: str

