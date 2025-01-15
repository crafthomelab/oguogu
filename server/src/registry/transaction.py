import asyncio
from datetime import datetime
import time
from typing import List, Optional
from hexbytes import HexBytes
import pytz
from src.abis.constants import OGUOGU_EVENT_ABI
from src.settings import Settings
from src.utils import create_signature
from web3 import Web3, AsyncWeb3
from eth_account import Account
from web3.contract.contract import ContractFunction, ContractEvent, Contract
from web3.types import TxReceipt, EventData
import logging

logger = logging.getLogger(__name__)

class TransactionManager:
    """ 
    TransactionManager is a class that send transaction to the blockchain.
    """
    def __init__(self, settings: Settings):
        self.operator = Account.from_key(settings.OPERATOR_PRIVATE_KEY)
        self.web3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URL))
        self.aweb3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(settings.WEB3_PROVIDER_URL))
        self.contract = self.web3.eth.contract(
            address=settings.OGUOGU_ADDRESS,
            abi=OGUOGU_EVENT_ABI
        )
        
    def oguogu_contract(self) -> Contract:
        return self.contract
        
    def get_events_from_transaction(
        self, 
        transaction_hash: str, 
        contract_event: ContractEvent,
    ) -> List[EventData]:
        logger.info(f"get_events_from_transaction {transaction_hash}")
        receipt = self.wait_tx_receipt(transaction_hash)
        
        events = []
        for log in receipt['logs']:
            try:
                event = contract_event.process_log(log)
                events.append(event)
            except Exception as e:
                logger.info(f"skip {log}")
                continue
        return events
    
    def create_signature(self, challenge_hash: str, account: Account=None) -> HexBytes:
        logger.info(f"create_signature {challenge_hash}")
        account = self.operator if account is None else account
        return create_signature(account, challenge_hash)
        
    async def aget_events_from_transcation(
        self, 
        transaction_hash,
        contract_event: ContractEvent,
    ) -> List[EventData]:
        logger.info(f"aget_event_from_transcation {transaction_hash}")
        receipt = await self.await_tx_receipt(transaction_hash)
        
        events = []
        for log in receipt['logs']:
            try:
                event = contract_event.process_log(log)
                events.append(event)
            except Exception as e:
                logger.info(f"skip {log}")
                continue
        return events

    def send_transaction(
        self,
        func: ContractFunction,
        account: Account = None,
    ) -> TxReceipt:
        logger.info(f"send_transaction {func}")
        account = self.operator if account is None else account
        
        nonce = self.web3.eth.get_transaction_count(account.address)
        tx = func.build_transaction({'from': account.address, 'nonce': nonce})
        signed_txn = account.sign_transaction(tx)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(txn_hash)
        
        verify_transaction(tx_receipt)
        return tx_receipt    
        
        
    async def asend_transaction(
        self,
        func: ContractFunction,
        account: Account = None,
    ) -> TxReceipt:
        logger.info(f"asend_transaction {func}")
        if account is None:
            account = self.operator
            
        nonce = await self.aweb3.eth.get_transaction_count(account.address)
        tx = func.build_transaction({ 'from': account.address, 'nonce': nonce })
        signed_txn = account.sign_transaction(tx)
        
        txn_hash = await self.aweb3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = await self.aweb3.eth.wait_for_transaction_receipt(txn_hash)
        
        verify_transaction(tx_receipt)
        return tx_receipt    
    
    def get_txreceipt_datetime(self, tx_receipt: TxReceipt) -> Optional[datetime]:
        logger.info(f"get_txreceipt_datetime {tx_receipt}")
        try:
            block = self.web3.eth.get_block(tx_receipt.blockNumber)
            return datetime.fromtimestamp(block.timestamp, tz=pytz.utc)
        except Exception as e:
            logger.error(f"Failed to get tx receipt datetime: {e}")
            return None
    
    async def aget_txreceipt_datetime(self, tx_receipt: TxReceipt) -> Optional[datetime]:
        logger.info(f"aget_txreceipt_datetime {tx_receipt}")
        try:
            block = await self.aweb3.eth.get_block(tx_receipt.blockNumber)
            return datetime.fromtimestamp(block.timestamp, tz=pytz.utc)
        except Exception as e:
            logger.error(f"Failed to get tx receipt datetime: {e}")
            return None
    
    def wait_tx_receipt(
        self, 
        transaction_hash: str,
        timeout: float = 120,
        poll_latency: float = 0.1,
    ) -> bool:
        """ 트랜잭션 수행 후, 트랜잭션 수행 결과를 반환합니다 """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                receipt = self.web3.eth.get_transaction_receipt(transaction_hash)
                if receipt is not None:
                    return receipt
            except Exception:
                continue
            time.sleep(poll_latency)
        raise Exception(f"Timeout waiting for transaction receipt {transaction_hash}")        
    
    
    async def await_tx_receipt(
        self, 
        transaction_hash: str,
        timeout: float = 120,
        poll_latency: float = 0.1,
    ) -> bool:
        """ 트랜잭션 수행 후, 트랜잭션 수행 결과를 반환합니다 """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                receipt = await self.aweb3.eth.get_transaction_receipt(transaction_hash)
                if receipt is not None:
                    return receipt
            except Exception:
                continue
            await asyncio.sleep(poll_latency)
        
        raise Exception(f"Timeout waiting for transaction receipt {transaction_hash}")        

def verify_transaction(tx_receipt: TxReceipt) -> bool:
    if tx_receipt.status != 1:
        raise Exception(f"Failed to send transaction.. status: {tx_receipt.status} tx_hash: {tx_receipt.transactionHash}")
    return True
