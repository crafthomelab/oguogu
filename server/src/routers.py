from datetime import datetime
from typing import Annotated, List, Literal, Optional
from eth_typing import ChecksumAddress
from fastapi import APIRouter, Depends, Form, UploadFile
from dependency_injector.wiring import Provide, inject
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.container import AppContainer
from src.domains import Challenge, ChallengeActivity, ChallengeSignature
from src.exceptions import ClientException
from src.registry.challenge import ChallengeRegistryService
from pydantic import BaseModel, Field
from src.registry.activity import ActivityRegistryService
from src.registry.reward import ChallengeRewardService
from src.utils import generate_photo_activity, recover_address


RegistryDependency = Depends(Provide[AppContainer.registry.registry])
ActivityDependency = Depends(Provide[AppContainer.registry.activity])
RewardDependency = Depends(Provide[AppContainer.registry.reward])


class ChallengeListDTO(BaseModel):
    """ Challenge List DTO """
    challenges: List['ChallengeDTO'] = Field(description="Challenges")
    
    @staticmethod
    def from_domain(challenges: List[Challenge]) -> 'ChallengeListDTO':
        return ChallengeListDTO(
            challenges=[ChallengeDTO.from_domain(challenge) for challenge in challenges]
        )

class ChallengeDTO(BaseModel):
    """ Challenge DTO """
    hash: str = Field(description="Challenge Hash")
    id: Optional[int] = Field(description="Challenge ID")
    nonce: int = Field(description="Nonce")
    status: str = Field(description="Challenge Status")
    
    challenger_address: str = Field(description="Challenger Address")
    reward_amount: str = Field(description="Reward Amount")
    
    title: str = Field(description="Challenge Title")
    type: Literal["photos"] = Field(description="Challenge Type")
    
    start_date: datetime = Field(description="Challenge Start Date")
    end_date: datetime = Field(description="Challenge End Date")
    minimum_activity_count: int = Field(description="Minimum Activity Count", examples=[3])
    
    activities: List['ActivityDTO'] = Field(description="Activities")
    
    payment_transaction: Optional[str] = Field(description="Payment Transaction")
    payment_reward: str = Field(description="Payment Reward")
    complete_date: Optional[datetime] = Field(description="Challenge Complete Date")
    
    @staticmethod
    def from_domain(challenge: Challenge) -> 'ChallengeDTO':
        return ChallengeDTO(
            hash=challenge.hash,
            id=challenge.id,
            nonce=challenge.nonce,
            status=challenge.status.value,
            challenger_address=challenge.challenger_address,
            reward_amount=str(int(challenge.reward_amount)),
            title=challenge.title,
            type=challenge.type.name,
            start_date=challenge.start_date,
            end_date=challenge.end_date,
            minimum_activity_count=challenge.minimum_activity_count,
            activities=[ActivityDTO.from_domain(activity) for activity in challenge.activities],
            payment_transaction=challenge.payment_transaction,
            payment_reward=str(int(challenge.payment_reward)),
            complete_date=challenge.complete_date,
        )


class ActivityDTO(BaseModel):
    """ Activity DTO """
    activity_hash: str = Field(description="Activity Hash")
    activity_date: datetime = Field(description="Activity Date")

    content_type: Optional[str] = Field(description="Content Type")
    image: Optional[str] = Field(description="base64 encoded JPEG image")
    screenshot_date: Optional[str] = Field(description="Screenshot Date")
    
    @staticmethod
    def from_domain(activity: ChallengeActivity) -> 'ActivityDTO':
        return ActivityDTO(
            activity_hash=activity.activity_hash,
            activity_date=activity.activity_date,
            content_type=activity.content.get("content_type"),
            image=activity.content.get("image"),
            screenshot_date=activity.content.get("screenshot_date"),
        )


class ChallengeCreateDTO(BaseModel):
    """ Challenge Create DTO """
    nonce: int = Field(description="Nonce")
    title: str = Field(description="Challenge Title")
    type: Literal['photos'] = Field(description="Challenge Type")
    reward_amount: str = Field(description="Reward Amount")
    start_date: datetime = Field(description="Challenge Start Date")
    end_date: datetime = Field(description="Challenge End Date")
    minimum_activity_count: int = Field(description="Minimum Activity Count")


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
    
class ActivityHashDTO(BaseModel):
    """ Activity Hash DTO """
    activity_hash: str = Field(description="Activity Hash")


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
@inject
async def get_challenge(
    user_address: Annotated[ChecksumAddress, Depends(authenticate_by_signature)],
    challenge_hash: str,
    registry: ChallengeRegistryService = RegistryDependency
) -> ChallengeDTO:
    challenge = await registry.get_user_challenge(user_address, challenge_hash)
    return ChallengeDTO.from_domain(challenge)


@router.get("/challenges")
@inject
async def get_challenges(
    user_address: Annotated[ChecksumAddress, Depends(authenticate_by_signature)],
    registry: ChallengeRegistryService = RegistryDependency
) -> ChallengeListDTO:
    challenges = await registry.get_active_challenges(user_address)
    return ChallengeListDTO.from_domain(challenges)

@router.post("/challenges")
@inject
async def create_challenge(
    user_address: Annotated[ChecksumAddress, Depends(authenticate_by_signature)],
    challenge: ChallengeCreateDTO,
    registry: ChallengeRegistryService = RegistryDependency
) -> ChallengeSignatureDTO:
    challenge = Challenge.new(
        nonce=challenge.nonce,
        challenger_address=user_address,
        reward_amount=int(challenge.reward_amount),
        title=challenge.title,
        type=challenge.type,
        start_date=challenge.start_date,
        end_date=challenge.end_date,
        minimum_activity_count=challenge.minimum_activity_count
    )
    
    signature = await registry.sign_new_challenge(challenge)
    return ChallengeSignatureDTO.from_domain(signature)


@router.post("/challenges/{challenge_hash}/register")
@inject
async def register_challenge(
    challenge_hash: str,
    request: ChallengeRegisterDTO,
    registry: ChallengeRegistryService = RegistryDependency
) -> OkResponse:
    await registry.register_challenge(request.transaction_hash)
    return OkResponse(ok=True)


@router.post("/challenges/{challenge_hash}/photo-activities")
@inject
async def register_photo_activity(
    challenge_hash: str,
    activity_file: UploadFile,
    registry: ChallengeRegistryService = RegistryDependency,
    activity_service: ActivityRegistryService = ActivityDependency
) -> ActivityHashDTO:
    activity_content = await generate_photo_activity(activity_file)
    
    if activity := await activity_service.find_activity(challenge_hash, activity_content.activity_hash):
        if activity.is_completed():
            raise ClientException(message="이미 제출한 제출물이에요.")
    
    challenge = await registry.get_challenge(challenge_hash)
    
    await activity_service.register_activity(challenge, activity_content)
    activity = ChallengeActivity.new(activity_content)
    return ActivityHashDTO(activity_hash=activity.activity_hash)


@router.get("/challenges/{challenge_hash}/photo-activities/{activity_hash}")
@inject
async def get_photo_activity(
    challenge_hash: str,
    activity_hash: str,
    user_address: Annotated[ChecksumAddress, Depends(authenticate_by_signature)],
    registry: ChallengeRegistryService = RegistryDependency,
    activity_service: ActivityRegistryService = ActivityDependency
) -> StreamingResponse:
    challenge = await registry.get_challenge(challenge_hash)
    
    if challenge.challenger_address != user_address:
        raise ClientException(message="접근 권한이 없어요.")
    
    activity = await activity_service.find_activity(challenge_hash, activity_hash)
    
    if activity is None:
        raise ClientException(message="존재하지 않은 제출물이에요.")
    
    stream_body = await activity_service.stream_activity_image(challenge_hash, activity_hash)
    return StreamingResponse(
        content=stream_body,
        media_type=activity.content.get("content_type")
    )


@router.post("/challenges/{challenge_hash}/photo-activities/{activity_hash}")
@inject
async def submit_photo_activity(
    challenge_hash: str,
    activity_hash: str,
    activity_signature: str = Form(..., description="Activity Signature"),
    registry: ChallengeRegistryService = RegistryDependency,
    activity_service: ActivityRegistryService = ActivityDependency
) -> OkResponse:
    challenge = await registry.get_challenge(challenge_hash)
    await activity_service.submit_activity(challenge, activity_hash, activity_signature)
    return OkResponse(ok=True)


@router.post("/challenges/{challenge_hash}/complete")
@inject
async def complete_challenge(
    challenge_hash: str,
    reward: ChallengeRewardService = RewardDependency
) -> ChallengeDTO:
    challenge = await reward.complete_challenge(challenge_hash)
    return ChallengeDTO.from_domain(challenge)
