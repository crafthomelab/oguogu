from datetime import datetime
from typing import List
from sqlalchemy import DateTime, Numeric, PrimaryKeyConstraint, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship, backref

from src.domains import Challenge, ChallengeActivity, ChallengeStatus, ChallengeType

class Base(AsyncAttrs, DeclarativeBase):
    pass


class ChallengeEntity(Base):
    __tablename__ = "challenges"

    hash: Mapped[str] = mapped_column(String, primary_key=True)
    id: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String)
    nonce: Mapped[int] = mapped_column(Integer)
    challenger_address: Mapped[str] = mapped_column(String)
    reward_amount: Mapped[int] = mapped_column(Numeric(precision=78, scale=0))

    title: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    minimum_activity_count: Mapped[int] = mapped_column(Integer)
    
    payment_transaction: Mapped[str] = mapped_column(String, nullable=True)
    payment_reward: Mapped[int] = mapped_column(Integer)
    complete_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    activities: Mapped[List["ChallengeActivityEntity"]] = relationship(
        "ChallengeActivityEntity", 
        backref=backref("challenge", lazy="joined"), 
        lazy="select"
    )
    
    @staticmethod
    def from_domain(domain: Challenge) -> "ChallengeEntity":
        return ChallengeEntity(
            hash=domain.hash,
            id=domain.id,
            nonce=domain.nonce,
            status=domain.status.value,
            challenger_address=domain.challenger_address,
            reward_amount=domain.reward_amount,
            title=domain.title,
            type=domain.type.name,
            start_date=domain.start_date,
            end_date=domain.end_date,
            minimum_activity_count=domain.minimum_activity_count,
            payment_transaction=domain.payment_transaction,
            payment_reward=domain.payment_reward,
            complete_date=domain.complete_date,
        )

    def to_domain(self) -> Challenge:
        return Challenge(
            hash=self.hash,
            id=self.id,
            nonce=self.nonce,
            status=ChallengeStatus(self.status),
            challenger_address=self.challenger_address,
            reward_amount=self.reward_amount,
            title=self.title,
            type=ChallengeType[self.type],
            start_date=self.start_date,
            end_date=self.end_date,
            minimum_activity_count=self.minimum_activity_count,
            payment_transaction=self.payment_transaction,
            payment_reward=self.payment_reward,
            complete_date=self.complete_date,
            activities=[activity.to_domain() for activity in self.activities],
        )


class ChallengeActivityEntity(Base):
    __tablename__ = "challenge_activities"

    activity_hash: Mapped[str] = mapped_column(String)
    challenge_hash: Mapped[str] = mapped_column(String, ForeignKey("challenges.hash"))
    
    activity_transaction: Mapped[str] = mapped_column(String, nullable=True)
    activity_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        PrimaryKeyConstraint('activity_hash', 'challenge_hash'),
    )    

    @staticmethod
    def from_domain(challenge_hash: str, domain: ChallengeActivity) -> "ChallengeActivityEntity":
        return ChallengeActivityEntity(
            challenge_hash=challenge_hash,
            activity_hash=domain.activity_hash,
            activity_transaction=domain.activity_transaction,
            activity_date=domain.activity_date,
        )
        
    def to_domain(self) -> ChallengeActivity:
        return ChallengeActivity(
            activity_hash=self.activity_hash,
            activity_transaction=self.activity_transaction,
            activity_date=self.activity_date,
        )