from datetime import datetime
from typing import Any, Dict, Literal, Union
from eth_typing import ChecksumAddress
from fastapi import UploadFile
from hexbytes import HexBytes
from web3 import Web3, AsyncWeb3
from eth_account import Account
from eth_account.messages import encode_defunct
from web3.contract.contract import ContractFunction
from web3.types import TxReceipt
from typing import Optional
from eth_abi.packed import encode_packed
    
def create_hash(**kwargs) -> bytes:
    """ 챌린지 해시를 생성합니다 """
    data_string = ''.join(f'{key}:{value}' for key, value in sorted(kwargs.items()))
    data_bytes = data_string.encode('utf-8')
    return Web3.to_hex(to_bytes32(Web3.keccak(data_bytes)))


def calculate_challenge_hash(
    title:str, 
    reward:int, 
    challenge_type: Literal["photos"], 
    challenger:Union[str, ChecksumAddress], 
    start_date:datetime, 
    end_date:datetime, 
    nonce:int, 
    minimum_activity_count:int
):
    # Web3.py를 사용하여 이더리움 주소를 체크섬 주소로 변환
    challenger = Web3.to_checksum_address(challenger)
    
    if challenge_type == 'photos':
        challenge_type = 0
    else:
        raise ClientException("Invalid challenge type")
    
    # abi.encodePacked와 동일한 방식으로 데이터를 인코딩
    encoded_data = encode_packed(
        ['string', 'uint256', 'uint8', 'address', 'uint256', 'uint256', 'uint32', 'uint8'],
        [title, reward, challenge_type, challenger, int(start_date.timestamp()), int(end_date.timestamp()), nonce, minimum_activity_count]
    )
    
    # keccak256 해시 생성
    challenge_hash = Web3.keccak(encoded_data)
    return Web3.to_hex(challenge_hash)



def create_signature(signer: Account, hash_value: Union[bytes, str]) -> HexBytes:
    """ 챌린지 해시에 서명합니다. """
    if isinstance(hash_value, str):
        message = encode_defunct(hexstr=hash_value)
    else:
        message = encode_defunct(hash_value)
    return signer.sign_message(message).signature


def recover_address(message: bytes, signature: bytes) -> str:
    if isinstance(message, str) and message.startswith("0x"):
        message = encode_defunct(hexstr=message)
    elif isinstance(message, str):
        message = encode_defunct(text=message)
    else:
        message = encode_defunct(message)

    if isinstance(signature, str):
        signature = HexBytes(signature)

    return Account.recover_message(message, signature=signature)


def verify_signature(
    signer_address: str, 
    signature: bytes, 
    hash_value: bytes
) -> bool:
    """ 서명을 검증합니다 """
    return recover_address(hash_value, signature) == signer_address


def verify_hash(challenge_data: Dict[str, Any], hash: bytes) -> bool:
    """ 챌린지 해시를 검증합니다 """    
    return create_hash(**challenge_data) == hash


def to_bytes32(value: Union[Dict, str, int, bytes]) -> bytes:
    """ bytes32 타입으로 변환합니다 """
    if isinstance(value, str):
        return value.encode("utf-8").ljust(32, b"\0")
    elif isinstance(value, int):
        return value.to_bytes(32, byteorder='big')
    elif isinstance(value, bytes):
        return value.ljust(32, b"\0")
    else:
        raise ValueError(f"Invalid type: {type(value)}")



def send_transaction(
    web3: Web3, 
    account: Account, 
    func: ContractFunction
) -> TxReceipt:
    nonce = web3.eth.get_transaction_count(account.address)
    tx = func.build_transaction({'from': account.address, 'nonce': nonce})
    signed_txn = account.sign_transaction(tx)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    return web3.eth.wait_for_transaction_receipt(txn_hash)
    
    
async def asend_transaction(
    web3: AsyncWeb3, 
    account: Account, 
    func: ContractFunction
) -> TxReceipt:
    nonce = await web3.eth.get_transaction_count(account.address)
    tx = func.build_transaction({ 'from': account.address, 'nonce': nonce })
    signed_txn = account.sign_transaction(tx)
    txn_hash = await web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = await web3.eth.wait_for_transaction_receipt(txn_hash)
    
    if tx_receipt.status != 1:
        raise Exception(f"Failed to send transaction.. status: {tx_receipt.status} tx_hash: {txn_hash}")
    
    return tx_receipt


async def generate_photo_activity(activity_file: UploadFile) -> dict:
    content_type = activity_file.content_type
    image_bytes = await activity_file.read()
    image = encode_image_url(content_type, image_bytes)
    screenshot_date = extract_screenshot_date(image_bytes)
    return {
        "image": image,
        "content_type": content_type,
        "screenshot_date": screenshot_date
    }


def extract_screenshot_date(image_bytes: bytes) -> Optional[str]:
    from PIL import Image
    from io import BytesIO
    
    image = Image.open(BytesIO(image_bytes))
    exif_data = image._getexif()
    if exif_data is not None:
        return exif_data.get(36867)

def encode_image_url(
    content_type: str,
    image_bytes: bytes
):
    import base64
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    return f"data:{content_type};base64,{base64_image}"