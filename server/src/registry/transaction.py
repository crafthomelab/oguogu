from datetime import datetime
from typing import Any, Dict
import pytz
from src.settings import Settings
from web3 import Web3, AsyncWeb3
from eth_account import Account
from web3.contract.contract import ContractFunction
from web3.types import TxReceipt



class TransactionManager:
    """ 
    TransactionManager is a class that send transaction to the blockchain.
    """
    def __init__(self, settings: Settings):
        self.operator = Account.from_key(settings.OPERATOR_PRIVATE_KEY)
        self.web3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URL))
        self.aweb3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(settings.WEB3_PROVIDER_URL))


    def send_transaction(
        self,
        func: ContractFunction,
        account: Account = None,
    ) -> TxReceipt:
        if account is None:
            account = self.operator
        
        nonce = self.web3.eth.get_transaction_count(account.address)
        tx = func.build_transaction({'from': account.address, 'nonce': nonce})
        signed_txn = account.sign_transaction(tx)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(txn_hash)
        
        self._verify_transaction(tx_receipt)
        return tx_receipt    
        
        
    async def asend_transaction(
        self,
        func: ContractFunction,
        account: Account = None,
    ) -> TxReceipt:
        if account is None:
            account = self.operator
            
        nonce = await self.aweb3.eth.get_transaction_count(account.address)
        tx = func.build_transaction({ 'from': account.address, 'nonce': nonce })
        signed_txn = account.sign_transaction(tx)
        
        txn_hash = await self.aweb3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = await self.aweb3.eth.wait_for_transaction_receipt(txn_hash)
        
        self._verify_transaction(tx_receipt)
        return tx_receipt    
    
    async def aget_txreceipt_datetime(self, tx_receipt: TxReceipt) -> datetime:
        block = await self.aweb3.eth.get_block(tx_receipt.blockNumber)
        return datetime.fromtimestamp(block.timestamp, tz=pytz.utc)
    
    def _verify_transaction(self, tx_receipt: TxReceipt) -> bool:
        if tx_receipt.status != 1:
            raise Exception(f"Failed to send transaction.. status: {tx_receipt.status} tx_hash: {tx_receipt.transaction_hash}")
        return True