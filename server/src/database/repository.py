from contextlib import AbstractContextManager
from typing import Callable, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.database.entity import ChallengeEntity, ChallengeProofEntity
from src.domains import Challenge, ChallengeProof, ChallengeStatus


class ChallengeRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[AsyncSession]]):
        self.session_factory = session_factory
        
    async def get_challenge(self, challenge_hash: str) -> Optional[Challenge]:
        """ 챌린지 조회하기 """
        async with self.session_factory() as session:
            stmt = (
                select(ChallengeEntity)
                .options(selectinload(ChallengeEntity.proofs))
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
                .options(selectinload(ChallengeEntity.proofs))
                .where(ChallengeEntity.challenger_address == challenger_address)
            )
            
            if statuses is not None:
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
            
    async def update_challenge_status(self, challenge: Challenge) -> None:
        """ 챌린지 상태 업데이트하기 """
        async with self.session_factory() as session:
            stmt = (
                update(ChallengeEntity)
                .filter(ChallengeEntity.hash == challenge.hash)
                .values(status=challenge.status.value)
            )
            await session.execute(stmt)
            await session.commit()
            
    async def add_proof(self, challenge_hash: str, proof: ChallengeProof) -> None:
        """ 챌린지 증명 추가하기 """
        async with self.session_factory() as session:
            entity = ChallengeProofEntity.from_domain(challenge_hash, proof)
            session.add(entity)
            await session.commit()
            

    async def _exist_challenge(self, challenge_hash: str, session: AsyncSession) -> bool:
        stmt = select(ChallengeEntity).where(ChallengeEntity.hash == challenge_hash)
        result = await session.execute(stmt)
        return result.scalar_one_or_none() is not None
