import uuid

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import Base


class Factory(Base):
    __tablename__ = "factories"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String, index=True)
    address = Column(String)
    reviews = relationship("Review", back_populates="factory")


class FactoryCreate(BaseModel):
    name: str
    address: str


class Review(Base):
    __tablename__ = "reviews"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    rating = Column(Float)
    satisfaction_level = Column(String)
    factory_id = Column(UUID, ForeignKey("factories.id"))
    factory = relationship("Factory", back_populates="reviews")


class ReviewCreate(BaseModel):
    rating: float
    satisfaction_level: str
