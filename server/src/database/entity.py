from datetime import datetime
from typing import List
from sqlalchemy import DateTime, Numeric, String, Integer, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from src.domains import Challenge, ChallengeProof, ChallengeStatus


from sqlalchemy.orm import relationship, backref

class Base(AsyncAttrs, DeclarativeBase):
    pass


class ChallengeEntity(Base):
    __tablename__ = "challenges"

    hash: Mapped[str] = mapped_column(String, primary_key=True)
    id: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String)

    challenger_address: Mapped[str] = mapped_column(String)
    reward_amount: Mapped[int] = mapped_column(Numeric(precision=78, scale=0))

    title: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    minimum_proof_count: Mapped[int] = mapped_column(Integer)

    receipent_address: Mapped[str] = mapped_column(String)
    
    proofs: Mapped[List["ChallengeProofEntity"]] = relationship(
        "ChallengeProofEntity", 
        backref=backref("challenge", lazy="joined"), 
        lazy="select"
    )
    
    @staticmethod
    def from_domain(domain: Challenge) -> "ChallengeEntity":
        return ChallengeEntity(
            hash=domain.hash,
            id=domain.id,
            status=domain.status.value,
            challenger_address=domain.challenger_address,
            reward_amount=domain.reward_amount,
            title=domain.title,
            type=domain.type,
            description=domain.description,
            start_date=domain.start_date,
            end_date=domain.end_date,
            minimum_proof_count=domain.minimum_proof_count,
            receipent_address=domain.receipent_address,
        )

    def to_domain(self) -> Challenge:
        return Challenge(
            hash=self.hash,
            id=self.id,
            status=ChallengeStatus(self.status),
            challenger_address=self.challenger_address,
            reward_amount=self.reward_amount,
            title=self.title,
            type=self.type,
            description=self.description,
            start_date=self.start_date,
            end_date=self.end_date,
            minimum_proof_count=self.minimum_proof_count,
            receipent_address=self.receipent_address,
            proofs=[
                ChallengeProof(
                    proof_hash=p.proof_hash,
                    content=p.content,
                ) for p in self.proofs
            ],
        )


class ChallengeProofEntity(Base):
    __tablename__ = "challenge_proofs"

    proof_hash: Mapped[str] = mapped_column(String, primary_key=True)
    challenge_hash: Mapped[str] = mapped_column(String, ForeignKey("challenges.hash"))
    content: Mapped[dict] = mapped_column(JSON)

    @staticmethod
    def from_domain(challenge_hash: str, domain: ChallengeProof) -> "ChallengeProofEntity":
        return ChallengeProofEntity(
            challenge_hash=challenge_hash,
            proof_hash=domain.proof_hash,
            content=domain.content,
        )
        
