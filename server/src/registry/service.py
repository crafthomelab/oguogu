import asyncio
import time
from eth_account import Account
from src.abis.constants import OGUOGU_EVENT_ABI
from src.database.repository import ChallengeRepository
from src.domains import Challenge, ChallengeSignature
from src.settings import Settings
from src.utils import create_signature
from web3 import AsyncWeb3
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
        settings: Settings
    ):
        self.repository = repository
        self.operator = Account.from_key(settings.OPERATOR_PRIVATE_KEY)
        self.web3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(settings.WEB3_PROVIDER_URL))
        self.contract = self.web3.eth.contract(
            address=settings.OGUOGU_CONTRACT_ADDRESS,
            abi=OGUOGU_EVENT_ABI
        )
        
    async def sign_new_challenge(
        self, 
        challenge: Challenge
    ) -> ChallengeSignature:
        """ 새로운 챌린지를 생성하고 서명합니다 """
        logger.info(f"Creating challenge {challenge.hash} for {challenge.challenger_address}")
        
        await self.repository.create_challenge(challenge)
        signature = create_signature(self.operator, challenge.hash)
        
        return ChallengeSignature(
            challenge_hash=challenge.hash,
            signature=signature.to_0x_hex()
        )
    
    async def open_challenge(
        self, 
        transaction_hash: str,
    ):
        """ 챌린지를 엽니다 """
        logger.info(f"Opening challenge {transaction_hash}")
        receipt = await self.wait_for_tx(transaction_hash)
        
        for log in receipt['logs']:
            try:
                event = self.contract.events.ChallengeCreated().process_log(log)
            except Exception as e:
                logger.info(f"skip {log}")
                continue

            challenge_hash = event['args']['challengeHash']
            challenge = await self.repository.get_challenge(challenge_hash)
            
            challenge.open(
                challenge_id=event['args']['tokenId'],
                challenger_address=event['args']['challenger']
            )

            await self.repository.open_challenge(challenge)
        
    async def wait_for_tx(
        self, 
        transaction_hash: str,
        timeout: float = 30,
        poll_latency: float = 1,
    ) -> bool:
        """ 트랜잭션 수행 후, 트랜잭션 수행 결과를 반환합니다 """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                receipt = await self.web3.eth.get_transaction_receipt(transaction_hash)
                if receipt is not None:
                    return receipt
            except Exception:
                continue
            await asyncio.sleep(poll_latency)
        
        raise Exception(f"Timeout waiting for transaction receipt {transaction_hash}")
        
        
        
        
        
        
        
        
    
    