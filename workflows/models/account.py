from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from base import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    initial_balance = Column(Float, nullable=False)
    current_balance = Column(Float, nullable=False)

    trades = relationship(
        "Trade",
        back_populates="account",
        cascade="all, delete, delete-orphan"
    )