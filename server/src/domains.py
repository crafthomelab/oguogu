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
    challenge_hash: bytes
    challenge_id: Optional[int]
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
            challenge_hash=challenge_hash,
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
        )

    def open(
        self, 
        challenge_id: int,
        challenger_address: str
    ):
        self.challenge_id = challenge_id
        self.challenger_address = Web3.to_checksum_address(challenger_address)
        self.status = ChallengeStatus.OPEN
        
    def add_proof(self, content: Dict[str, any]) -> bool:
        if self.status != ChallengeStatus.OPEN:
            raise ValueError("only allow open challenge")
        
        self.proofs.append(
            ChallengeProof.new(content)
        )
        return len(self.proofs) >= self.minimum_proof_count        
        
    def success(self):
        self.status = ChallengeStatus.SUCCESS

    def fail(self):
        self.status = ChallengeStatus.FAILED


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
    
    @staticmethod
    def new(content: Dict[str, any]) -> "ChallengeProof":
        proof_hash = create_hash(**content)
        return ChallengeProof(
            proof_hash=proof_hash, 
            content=content
        )