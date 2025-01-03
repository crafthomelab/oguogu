from datetime import datetime
from typing import Annotated, List, Optional
from eth_typing import ChecksumAddress
from fastapi import APIRouter, Depends, Form, UploadFile
from dependency_injector.wiring import Provide
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.container import AppContainer
from src.domains import Challenge, ChallengeProof, ChallengeSignature
from src.registry.challenge import ChallengeRegistryService
from pydantic import BaseModel, Field
from src.registry.proof import ProofRegistryService
from src.registry.reward import ChallengeRewardService
from src.utils import recover_address


RegistryDependency = Depends(Provide[AppContainer.registry.registry])
ProofDependency = Depends(Provide[AppContainer.registry.proof])
RewardDependency = Depends(Provide[AppContainer.registry.reward])


class ChallengeDTO(BaseModel):
    """ Challenge DTO """
    hash: str = Field(description="Challenge Hash")
    id: Optional[int] = Field(description="Challenge ID")
    status: str = Field(description="Challenge Status")
    
    challenger_address: str = Field(description="Challenger Address")
    reward_amount: str = Field(description="Reward Amount")
    
    title: str = Field(description="Challenge Title")
    type: str = Field(description="Challenge Type")
    description: str = Field(description="Challenge Description")
    
    start_date: datetime = Field(description="Challenge Start Date")
    end_date: datetime = Field(description="Challenge End Date")
    minimum_proof_count: int = Field(description="Minimum Proof Count")
    
    receipent_address: str = Field(description="Receipent Address")
    proofs: List['ProofDTO'] = Field(description="Proofs")
    
    payment_transaction: Optional[str] = Field(description="Payment Transaction")
    payment_reward: str = Field(description="Payment Reward")
    complete_date: Optional[datetime] = Field(description="Challenge Complete Date")
    
    @staticmethod
    def from_domain(challenge: Challenge) -> 'ChallengeDTO':
        return ChallengeDTO(
            hash=challenge.hash,
            id=challenge.id,
            status=challenge.status.value,
            challenger_address=challenge.challenger_address,
            reward_amount=str(challenge.reward_amount),
            title=challenge.title,
            type=challenge.type,
            description=challenge.description,
            start_date=challenge.start_date,
            end_date=challenge.end_date,
            minimum_proof_count=challenge.minimum_proof_count,
            receipent_address=challenge.receipent_address,
            proofs=[ProofDTO.from_domain(proof) for proof in challenge.proofs],
            payment_transaction=challenge.payment_transaction,
            payment_reward=str(challenge.payment_reward),
            complete_date=challenge.complete_date,
        )


class ProofDTO(BaseModel):
    """ Proof DTO """
    proof_hash: str = Field(description="Proof Hash")
    proof_date: datetime = Field(description="Proof Date")

    content_type: Optional[str] = Field(description="Content Type")
    image_bytes: Optional[str] = Field(description="base64 encoded JPEG image")
    
    @staticmethod
    def from_domain(proof: ChallengeProof) -> 'ProofDTO':
        return ProofDTO(
            proof_hash=proof.proof_hash,
            proof_date=proof.proof_date,
            content_type=proof.content.get("content_type"),
            image_bytes=proof.content.get("image_bytes"),
        )


class ChallengeCreateDTO(BaseModel):
    """ Challenge Create DTO """
    title: str = Field(description="Challenge Title")
    type: str = Field(description="Challenge Type")
    reward_amount: int = Field(description="Reward Amount")
    description: str = Field(description="Challenge Description")
    end_date: datetime = Field(description="Challenge End Date")
    minimum_proof_count: int = Field(description="Minimum Proof Count")
    receipent_address: str = Field(description="Receipent Address")


class ChallengeSignatureDTO(BaseModel):
    """ Challenge Signature DTO """
    challenge_hash: str = Field(description="Challenge Hash")
    signature: str = Field(description="Signature")
    
    @staticmethod
    def from_domain(signature: ChallengeSignature) -> 'ChallengeSignatureDTO':
        return ChallengeSignatureDTO(
            challenge_hash=signature.challenge_hash,
            signature=signature.signature,
        )


class ChallengeRegisterDTO(BaseModel):
    """ Challenge Register DTO """
    transaction_hash: str = Field(description="Transaction Hash of Challenge Register")

class OkResponse(BaseModel):
    """ Ok Response """
    ok: bool = Field(description="OK")
    
class ProofHashDTO(BaseModel):
    """ Proof Hash DTO """
    proof_hash: str = Field(description="Proof Hash")


router = APIRouter()

security = HTTPBearer()


@router.get("/")
async def read_root():
    return {"message": "Oguogu API Server"}


def authenticate_by_signature(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> ChecksumAddress:
    token = credentials.credentials
    message, signature = token.split(":")
    return recover_address(message, signature)


@router.get("/challenges/{challenge_hash}")
async def get_challenge(
    user_address: Annotated[ChecksumAddress, Depends(authenticate_by_signature)],
    challenge_hash: str,
    registry: ChallengeRegistryService = RegistryDependency
) -> ChallengeDTO:
    challenge = await registry.get_user_challenge(user_address, challenge_hash)
    return ChallengeDTO.from_domain(challenge)


@router.get("/challenges")
async def get_challenges(
    user_address: Annotated[ChecksumAddress, Depends(authenticate_by_signature)],
    registry: ChallengeRegistryService = RegistryDependency
) -> List[ChallengeDTO]:
    challenges = await registry.get_active_challenges(user_address)
    return [
        ChallengeDTO.from_domain(challenge) for challenge in challenges
    ]

@router.post("/{user_address}/challenges")
async def create_challenge(
    user_address: Annotated[ChecksumAddress, Depends(authenticate_by_signature)],
    challenge: ChallengeCreateDTO,
    registry: ChallengeRegistryService = RegistryDependency
) -> ChallengeSignatureDTO:
    challenge = Challenge.new(
        challenger_address=user_address,
        reward_amount=challenge.reward_amount,
        title=challenge.title,
        type=challenge.type,
        description=challenge.description,
        end_date=challenge.end_date,
        minimum_proof_count=challenge.minimum_proof_count,
        receipent_address=challenge.receipent_address,
    )
    
    signature = await registry.sign_new_challenge(challenge)
    return ChallengeSignatureDTO.from_domain(signature)


@router.post("/challenges/{challenge_hash}/register")
async def register_challenge(
    challenge_hash: str,
    request: ChallengeRegisterDTO,
    registry: ChallengeRegistryService = RegistryDependency
) -> OkResponse:
    await registry.register_challenge(request.transaction_hash)
    return OkResponse(ok=True)


@router.post("/photo-proof/hash")
async def calculate_proof_hash(
    proof_file: UploadFile,
    proof: ProofRegistryService = ProofDependency
) -> ProofHashDTO:
    proof_content = {   
        "content_type": "image/jpeg",
        "image_bytes": await proof_file.read(),
    }
    proof_hash = proof.calculate_proof_hash(proof_content)    
    return ProofHashDTO(proof_hash=proof_hash)


@router.post("/challenges/{challenge_hash}/photo-proof")
async def submit_photo_proof(
    challenge_hash: str,
    proof_file: UploadFile,
    proof_signature: str = Form(..., description="Proof Signature"),
    registry: ChallengeRegistryService = RegistryDependency,
    proof: ProofRegistryService = ProofDependency
) -> OkResponse:
    challenge = await registry.get_challenge_by_hash(challenge_hash)
    proof_content = {   
        "content_type": "image/jpeg",
        "image_bytes": await proof_file.read(),
    }
    await proof.verify_proof(challenge, proof_content, proof_signature)
    await proof.submit_proof(challenge, proof_content, proof_signature)
    
    return OkResponse(ok=True)


@router.post("/challenges/{challenge_hash}/complete")
async def complete_challenge(
    challenge_hash: str,
    reward: ChallengeRewardService = RewardDependency
) -> ChallengeDTO:
    challenge = await reward.complete_challenge(challenge_hash)
    return ChallengeDTO.from_domain(challenge)
