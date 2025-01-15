from contextlib import AbstractContextManager
from typing import Callable, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.database.entity import ChallengeEntity, ChallengeActivityEntity
from src.domains import Challenge, ChallengeActivity, ChallengeStatus
from sqlalchemy.exc import IntegrityError
from src.exceptions import ClientException


class ChallengeRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[AsyncSession]]):
        self.session_factory = session_factory
        
    async def get_challenge_by_id(self, challenge_id: int) -> Optional[Challenge]:
        """ 챌린지 ID로 조회하기 """
        async with self.session_factory() as session:
            stmt = (
                select(ChallengeEntity)
                .options(selectinload(ChallengeEntity.activities))
                .where(ChallengeEntity.id == challenge_id)
            )
            result = await session.execute(stmt)
            challenge_entity = result.scalar_one_or_none()
            if challenge_entity is None:
                return None
            return challenge_entity.to_domain()
        
    async def get_challenge(self, challenge_hash: str) -> Optional[Challenge]:
        """ 챌린지 조회하기 """
        async with self.session_factory() as session:
            stmt = (
                select(ChallengeEntity)
                .options(selectinload(ChallengeEntity.activities))
                .where(ChallengeEntity.hash == challenge_hash)
            )
            result = await session.execute(stmt)
            challenge_entity = result.scalar_one_or_none()
            if challenge_entity is None:
                return None
            return challenge_entity.to_domain()
        
    async def get_challeges_by_challenger(
        self, 
        challenger_address: str,
        statuses: List[ChallengeStatus] = None
    ) -> List[Challenge]:
        """ 유저의 챌린지 목록 가져오기 """
        async with self.session_factory() as session:
            stmt = (
                select(ChallengeEntity)
                .options(selectinload(ChallengeEntity.activities))
                .where(ChallengeEntity.challenger_address == challenger_address)
            )
            
            if statuses is not None:
                statuses = [status.value for status in statuses]
                stmt = stmt.where(ChallengeEntity.status.in_(statuses))
            
            result = await session.execute(stmt)
            challenge_entities = result.scalars().all()
            challenges = [challenge_entity.to_domain() for challenge_entity in challenge_entities]
            return challenges
            
    async def create_challenge(self, challenge: Challenge) -> None:
        """ 챌린지 생성하기 """
        async with self.session_factory() as session:
            entity = ChallengeEntity.from_domain(challenge)
            session.add(entity)
            await session.commit()
            
    async def open_challenge(self, challenge: Challenge) -> None:
        """ 챌린지 공개하기 """
        async with self.session_factory() as session:
            stmt = (
                update(ChallengeEntity)
                .filter(ChallengeEntity.hash == challenge.hash)
                .values(
                    status=challenge.status.value,
                    challenger_address=challenge.challenger_address,
                    id=challenge.id,
                )
            )
            await session.execute(stmt)
            await session.commit()
            
    async def complete_challenge(self, challenge: Challenge) -> None:
        """ 챌린지 완료하기 """
        async with self.session_factory() as session:
            stmt = (
                update(ChallengeEntity)
                .filter(ChallengeEntity.hash == challenge.hash)
                .values(
                    status=challenge.status.value,
                    payment_transaction=challenge.payment_transaction,
                    payment_reward=challenge.payment_reward,
                    complete_date=challenge.complete_date
                )
            )
            await session.execute(stmt)
            await session.commit()
            
            
    async def find_activity(self, challenge_hash: str, activity_hash: str) -> Optional[ChallengeActivity]:
        """ 챌린지 증명 조회하기 """
        async with self.session_factory() as session:
            stmt = select(ChallengeActivityEntity).where(
                ChallengeActivityEntity.challenge_hash == challenge_hash, 
                ChallengeActivityEntity.activity_hash == activity_hash
            )
            result = await session.execute(stmt)
            activity_entity = result.scalar_one_or_none()
            if activity_entity:
                return activity_entity.to_domain()
            return None
            
    async def get_activity(self, challenge_hash: str, activity_hash: str) -> ChallengeActivity:
        """ 챌린지 증명 조회하기 """
        activity = await self.find_activity(challenge_hash, activity_hash)
        if activity is None:
            raise ClientException(message="존재하지 않은 제출물이에요.")
        return activity
            

    async def add_activity(self, challenge_hash: str, activity: ChallengeActivity) -> None:
        """ 챌린지 증명 제출하기 """
        async with self.session_factory() as session:
            entity = ChallengeActivityEntity.from_domain(challenge_hash, activity)
            session.add(entity)
            try:
                await session.commit()  
            except IntegrityError:
                await session.rollback()
                raise ClientException(message="이미 동일한 것이 제출되었어요.")


    async def complete_activity(self, challenge_hash: str, activity: ChallengeActivity) -> None:
        """ 챌린지 증명 완료하기 """
        async with self.session_factory() as session:
            stmt = (
                update(ChallengeActivityEntity)
                .filter(ChallengeActivityEntity.challenge_hash == challenge_hash, 
                        ChallengeActivityEntity.activity_hash == activity.activity_hash)
                .values(
                    activity_transaction=activity.activity_transaction, 
                    activity_date=activity.activity_date
                )
            )
            await session.execute(stmt)
            try:
                await session.commit()  
            except IntegrityError:
                await session.rollback()
                raise ClientException(message="이미 동일한 것이 제출되었어요.")
                        

    async def _exist_challenge(self, challenge_hash: str, session: AsyncSession) -> bool:
        stmt = select(ChallengeEntity).where(ChallengeEntity.hash == challenge_hash)
        result = await session.execute(stmt)
        return result.scalar_one_or_none() is not None
