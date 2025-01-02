from typing import Dict
from src.abis.constants import OGUOGU_EVENT_ABI
from src.database.repository import ChallengeRepository
from src.domains import Challenge, ChallengeProof
from src.registry.grader import ProofGrader
from src.registry.transaction import TransactionManager
from src.settings import Settings
from src.utils import create_hash, verify_signature
import logging

logger = logging.getLogger(__name__)


class ProofRegistryService:
    """ 챌린지 수행 증명 서비스
    
    [ PROCESS ]
        1. 유저가 수행하고, 증명 자료(ex: 캡처된 이미지)를 제출
        2. 서버는 증명 해시값을 계산해서 제공
        3. 유저는 증명 해시값에 서명하여 서버에게 전달
        4. 서버는 증명 해시값을 검증하고, 블록체인에 등록
    """
    def __init__(
        self, 
        repository: ChallengeRepository,
        transaction: TransactionManager,
        grader: ProofGrader,
        settings: Settings
    ):
        self.repository = repository
        self.transaction = transaction
        self.contract = self.transaction.web3.eth.contract(
            address=settings.OGUOGU_ADDRESS,
            abi=OGUOGU_EVENT_ABI
        )
        self.grader = grader
        
    def calculate_proof_hash(
        self,
        content: Dict[str, any],
    ) -> str:
        """ 챌린지 수행 증명 해시값을 계산합니다. """
        logger.info(f"calculate proof hash: {content}")
        return create_hash(**content)
        
    async def verify_proof(
        self,
        challenge: Challenge,
        proof_content: Dict[str, any],
        proof_signature: str,
    ) -> str:
        """ 챌린지 수행 증명을 검증합니다. """
        if not challenge.available_to_submit_proof():
            raise Exception("도전할 수 없는 챌린지입니다.")
        
        proof_hash = self.calculate_proof_hash(proof_content)

        if not verify_signature(
            challenge.challenger_address, 
            proof_hash, 
            proof_signature
        ):
            raise Exception("잘못된 서명입니다.")
        
        response = await self.grader.grade_proof(challenge, proof_content)
        if not response.is_correct:
            raise Exception(response.message)
        
        return response.message
        
        
    async def submit_proof(
        self,
        challenge: Challenge,
        proof_content: Dict[str, any],
        proof_signature: str,
    ):
        """ 챌린지 수행 증명을 제출합니다. """
        request = self.contract.functions.submitProof(
            challenge.id,
            self.calculate_proof_hash(proof_content),
            proof_signature,
        )
        
        tx_receipt = await self.transaction.asend_transaction(request)
        proof_date = await self.transaction.aget_txreceipt_datetime(tx_receipt)
        
        proof = ChallengeProof.new(proof_content, proof_date)
        await self.repository.add_proof(challenge.hash, proof)
        return proof