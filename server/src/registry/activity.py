from typing import Dict, Optional
from src.database.repository import ChallengeRepository
from src.domains import Challenge, ChallengeActivity
from src.exceptions import ClientException
from src.registry.grader import ActivityGrader
from src.registry.transaction import TransactionManager
from src.storage.repository import ObjectRepository
from src.utils import verify_signature
from aiobotocore.response import StreamingBody
import logging

logger = logging.getLogger(__name__)

class ActivityRegistryService:
    """ 챌린지 수행 증명 서비스
    
    [ PROCESS ]
        1. 유저가 수행하고, 증명 자료(ex: 캡처된 이미지)를 서버에 검증 요청
            - 서버는 판단하고 검증 결과를 반환
        2. 서버는 증명 해시값을 계산해서 제공
        3. 유저는 증명 해시값에 서명하여 서버에게 전달
        4. 서버는 증명 해시값을 검증하고, 블록체인에 등록
    """
    def __init__(
        self, 
        repository: ChallengeRepository,
        transaction: TransactionManager,
        storage: ObjectRepository,
        grader: ActivityGrader,
    ):
        self.repository = repository
        self.transaction = transaction
        self.storage = storage
        self.grader = grader
        self.submit_activity_function = transaction.oguogu_contract().functions.submitActivity        
        
    async def find_activity(self, challenge_hash: str, activity_hash: str) -> Optional[ChallengeActivity]:
        return await self.repository.find_activity(challenge_hash, activity_hash)
    
    async def stream_activity_image(self, challenge_hash: str, activity_hash: str) -> StreamingBody:
        return await self.storage.astream_by_id(f"{challenge_hash}/{activity_hash}")
                
    async def register_activity(self, challenge: Challenge, content: Dict[str, any]) -> str:
        """ 챌린지 수행 증명을 검증 후 등록합니다. """
        if not challenge.available_to_submit_activity():
            raise ClientException(message="도전할 수 없는 챌린지에요.")
        
        response = await self.grader.grade_activity(challenge, content)
        
        if not response.is_correct:
            raise ClientException(message=response.message)
        
        await self.storage.asave('oguogu', 
                                 content['image'], content['content_type'])
        activity = ChallengeActivity.new(content)
        await self.repository.add_activity(challenge.hash, activity)
        
        return response.message
        

    async def submit_activity(self, challenge: Challenge, activity_hash: str, activity_signature: str):
        """ 챌린지 수행 증명을 제출합니다. """
        if not verify_signature(challenge.challenger_address, activity_signature, activity_hash):
            raise ClientException(message="서명이 유효하지 않아요.")
        
        request = self.submit_activity_function(
            challenge.id,
            activity_hash,
            activity_signature,
        )
        
        activity = await self.repository.get_activity(challenge.hash, activity_hash)
        
        tx_receipt = await self.transaction.asend_transaction(request)
        activity_date = await self.transaction.aget_txreceipt_datetime(tx_receipt)
        
        tx_hash = tx_receipt['transactionHash'].to_0x_hex()
        activity.complete(tx_hash, activity_date)
        await self.repository.complete_activity(challenge.hash, activity)
        return activity