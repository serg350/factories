import enum
import uuid

from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum

from db.postgres import Base


class SatisfactionLevelEnum(enum.Enum):
    Great = 'Отлично'
    Normally = 'Нормально'
    Badly = 'Плохо'


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

    def __init__(self, name: str, address: str) -> None:
        self.name = name
        self.address = address


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
    rating = Column(Float, CheckConstraint('rating>=1 AND rating<=5'))
    satisfaction_level = Column(Enum(SatisfactionLevelEnum))
    factory_id = Column(UUID, ForeignKey("factories.id"))
    factory = relationship("Factory", back_populates="reviews")


class ReviewCreate(BaseModel):
    rating: float = Field(..., gt=0, lt=5.1, description='The rating must be between 1 and 5')
    satisfaction_level: SatisfactionLevelEnum = Field(...,
                                                      description="Satisfaction level must be one of "
                                                                  "[Great = 'Отлично', Normally = 'Нормально',"
                                                                  "Badly = 'Плохо'")
