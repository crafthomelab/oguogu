from typing import List, Optional
from eth_typing import ChecksumAddress
from src.database.repository import ChallengeRepository
from src.domains import Challenge, ChallengeSignature, ChallengeStatus
from src.exceptions import ClientException
from src.registry.transaction import TransactionManager
from web3 import Web3
import logging

logger = logging.getLogger(__name__)


class ChallengeRegistryService:
    """ 챌린지 등록 서비스
    
    [ PROCESS ]
        1. 유저가 챌린지 정보를 입력
        
        2. 유저 --> 서버로 챌린지 정보 전달. 그러면 서버는 서명된 챌린지 정보를 내려줌
        
        3. 유저가 서명된 챌린지 정보를 서명하여 Blockchain Network에 호출 (contract.openChallenge)
        
        4. 유저는 블록체인 TX 해시값을 서버로 전달
        
        5. 서버는 블록체인 TX 해시값을 통해, 올바르게 블록체인에 호출되었는지 확인
    """
    def __init__(
        self, 
        repository: ChallengeRepository,
        transaction: TransactionManager,
    ):
        self.repository = repository
        self.transaction = transaction
        self.challenge_created_event = transaction.oguogu_contract().events.ChallengeCreated()
        
    async def get_user_challenge(
        self, 
        user_address: ChecksumAddress,
        challenge_hash: str
    ) -> Challenge:
        challenge = await self.repository.get_challenge(challenge_hash)
        if challenge is None or challenge.challenger_address != user_address:
            raise Exception(f"Challenge {challenge_hash} not found")
        return challenge
    
    async def find_challenge(
        self, challenge_hash: str
    ) -> Optional[Challenge]:
        return await self.repository.get_challenge(challenge_hash)
        
    async def get_challenge(
        self, challenge_hash: str
    ) -> Challenge:
        challenge = await self.find_challenge(challenge_hash)
        if challenge is None:
            raise ClientException(message=f"Challenge {challenge_hash} not found")
        return challenge
    
    async def get_active_challenges(
        self,
        user_address: str,
    ) -> List[Challenge]:
        challenges = await self.repository.get_challeges_by_challenger(
            user_address, 
            [ChallengeStatus.OPEN, 
             ChallengeStatus.SUCCESS, 
             ChallengeStatus.FAILED]
        )
        return sorted(
            challenges, 
            key=lambda x: x.start_date, 
            reverse=True
        )
        
    async def sign_new_challenge(
        self, 
        challenge: Challenge,
        skip_create: bool = False
    ) -> ChallengeSignature:
        """ 새로운 챌린지를 생성하고 서명합니다 """
        logger.info(f"Creating challenge {challenge.hash} for {challenge.challenger_address}")
        
        if not skip_create:
            await self.repository.create_challenge(challenge)
        signature = self.transaction.create_signature(challenge.hash)
        
        return ChallengeSignature(
            challenge_hash=challenge.hash,
            signature=signature.to_0x_hex(),
            payload={
                "title": challenge.title,
                "reward": challenge.reward_amount,
                "type": challenge.type.value,
                "challenger": challenge.challenger_address,
                "startDate": int(challenge.start_date.timestamp()),
                "endDate": int(challenge.end_date.timestamp()),
                "nonce": challenge.nonce,
                "minimumActivityCount": challenge.minimum_activity_count
            }
        )
    
    async def register_challenge(
        self, 
        transaction_hash: str,
    ):
        """ 챌린지를 서버에 등록합니다. """
        logger.info(f"Opening challenge {transaction_hash}")
        
        events = await self.transaction.aget_events_from_transcation(
            transaction_hash,
            self.challenge_created_event
            )

        for event in events:
            challenge_hash = Web3.to_hex(event['args']['challengeHash'])
            challenge = await self.repository.get_challenge(challenge_hash)
            
            challenge.open(
                challenge_id=event['args']['tokenId'],
                challenger_address=event['args']['challenger']
            )

            await self.repository.open_challenge(challenge)
        
        
        
        
        
        
        
    
    