from datetime import datetime
from typing import Dict
from eth_account import Account
import pytz
from src.abis.constants import OGUOGU_EVENT_ABI
from src.database.repository import ChallengeRepository
from src.domains import Challenge, ChallengeProof
from src.settings import Settings
from src.utils import asend_transaction, create_hash, verify_signature
from web3 import AsyncWeb3
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
        settings: Settings
    ):
        self.repository = repository
        self.operator = Account.from_key(settings.OPERATOR_PRIVATE_KEY)
        self.web3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(settings.WEB3_PROVIDER_URL))
        self.contract = self.web3.eth.contract(
            address=settings.OGUOGU_ADDRESS,
            abi=OGUOGU_EVENT_ABI
        )
        
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
    ) -> bool:
        """ 챌린지 수행 증명을 검증합니다. """
        # 1. verify challenge
        if not challenge.available_to_submit_proof():
            raise Exception("Challenge is not available to submit proof")
        
        proof_hash = self.calculate_proof_hash(proof_content)

        # 2. verify signature
        if not verify_signature(
            challenge.challenger_address, 
            proof_hash, 
            proof_signature
        ):
            raise Exception("Invalid proof signature")
        
        # 3. verify proof on OpenAI Evaluator
        return True
        
        
    async def submit_proof(
        self,
        challenge: Challenge,
        proof_content: Dict[str, any],
        proof_signature: str,
    ):
        """ 챌린지 수행 증명을 제출합니다. """
        # 1. send proof to blockchain
        proof_hash = self.calculate_proof_hash(proof_content)
        
        tx_receipt = await asend_transaction(
            self.web3,
            self.operator,
            self.contract.functions.submitProof(
                challenge.id,
                proof_hash,
                proof_signature,
            )
        )
        
        if tx_receipt.status != 1:
            raise Exception("Failed to submit proof")
        
        # 2. get proof date
        block = await self.web3.eth.get_block(tx_receipt.blockNumber)
        proof_date = datetime.fromtimestamp(block.timestamp, tz=pytz.utc)
        
        # 3. add proof to database
        proof = ChallengeProof.new(proof_content, proof_date)
        await self.repository.add_proof(challenge.hash, proof)
        return proof