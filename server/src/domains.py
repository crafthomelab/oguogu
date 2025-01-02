from dataclasses import dataclass
from typing import Dict, List, Literal, Optional
from datetime import datetime
import pytz
from web3 import Web3
from enum import Enum

from src.utils import create_hash


@dataclass
class Challenge:
    """ Challenge 도메인 """
    hash: str
    id: Optional[int]
    status: "ChallengeStatus"
    
    challenger_address: str
    reward_amount: int
    
    title: str
    type: Literal["photos"]
    description: str
    
    start_date: datetime
    end_date: datetime
    minimum_proof_count: int
    
    receipent_address: str
    proofs: List["ChallengeProof"]
    
    payment_transaction: Optional[str] = None
    complete_date: Optional[datetime] = None
    
    @staticmethod
    def new(
        challenger_address: str,
        reward_amount: int,
        title: str,
        type: Literal["photos"],
        description: str,
        end_date: datetime,
        minimum_proof_count: int,
        receipent_address: str,
    ) -> "Challenge":
        if reward_amount <= 0:
            raise ValueError("Reward amount must be greater than 0")
        
        start_date = datetime.now(pytz.utc)
        if end_date < start_date:
            raise ValueError("End date must be greater than current time")
        
        if minimum_proof_count <= 0:
            raise ValueError("Minimum proof count must be greater than 0")
        
        if type != "photos":
            raise ValueError("Invalid challenge type")
        
        if not Web3.is_address(receipent_address):
            raise ValueError("Invalid receipent address")
        receipent_address = Web3.to_checksum_address(receipent_address)
        
        if not Web3.is_address(challenger_address):
            raise ValueError("Invalid challenger address")
        challenger_address = Web3.to_checksum_address(challenger_address)
        
        challenge_hash = create_hash(
            challenger_address=challenger_address,
            reward_amount=reward_amount,
            title=title,
            type=type,
            description=description,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            minimum_proof_count=minimum_proof_count,
            receipent_address=receipent_address,
        )
        
        return Challenge(
            id=None,
            hash=Web3.to_hex(challenge_hash),
            status=ChallengeStatus.INIT,
            challenger_address=challenger_address,
            reward_amount=reward_amount,
            title=title,
            type=type,
            description=description,
            start_date=start_date,
            end_date=end_date,
            minimum_proof_count=minimum_proof_count,
            receipent_address=receipent_address,
            proofs=[],
            payment_transaction=None,
            complete_date=None,
        )
        
    def available_to_submit_proof(self) -> bool:
        return (
            self.status == ChallengeStatus.OPEN
            and self.end_date >= datetime.now(pytz.utc)
            and len(self.proofs) < self.minimum_proof_count
        )   
        
    def available_to_complete(self) -> bool:
        """ 챌린지 완료 처리 가능한지 여부 """
        if self.status != ChallengeStatus.OPEN:
            return False
        
        if len(self.proofs) >= self.minimum_proof_count:
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
        
    def success(self, payment_transaction: str, complete_date: datetime=None):        
        if complete_date is None:
            complete_date = datetime.now(pytz.utc)
        self.status = ChallengeStatus.SUCCESS
        self.payment_transaction = payment_transaction
        self.complete_date = complete_date
    
    def fail(self, payment_transaction: str, complete_date: datetime=None):
        if complete_date is None:
            complete_date = datetime.now(pytz.utc)
        self.status = ChallengeStatus.FAILED
        self.payment_transaction = payment_transaction
        self.complete_date = complete_date
        


class ChallengeStatus(Enum):
    """ 챌린지 상태 """
    INIT = 'INIT' # challenge signature 생성된 상태
    OPEN = 'OPEN' # challenge가 Network에 등록된 상태
    SUCCESS = 'SUCCESS' # challenge가 성공한 상태
    FAILED = 'FAILED' # challenge가 실패한 상태    


@dataclass
class ChallengeProof:
    """ 챌린지 수행 증명 자료 """
    proof_hash: str
    content: Dict[str, any]
    proof_date: datetime
    
    @staticmethod
    def new(content: Dict[str, any], proof_date: datetime=None) -> "ChallengeProof":
        if proof_date is None:
            proof_date = datetime.now(pytz.utc)
        proof_hash = create_hash(**content)
        return ChallengeProof(
            proof_hash=Web3.to_hex(proof_hash), 
            content=content,
            proof_date=proof_date
        )

@dataclass
class ChallengeSignature:
    """ 챌린지 서명 도메인 """
    challenge_hash: str
    signature: str

