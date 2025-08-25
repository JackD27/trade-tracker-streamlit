from datetime import datetime

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship

from .base import Base

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))
    security_id = Column(Integer, ForeignKey("securities.id"))
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=False)
    fees = Column(Float, default=0.0, nullable=False)
    quantity = Column(Integer, nullable=False)
    entry_date = Column(DateTime, default=datetime.utcnow)
    exit_date = Column(DateTime, nullable=True)
    details = Column(String, default="")

    account = relationship("Account", back_populates="trades")
    security = relationship("Security")