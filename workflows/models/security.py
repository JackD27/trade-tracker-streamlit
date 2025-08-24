from sqlalchemy import Column, Integer, String
from base import Base

class Security(Base):
    __tablename__ = "securities"

    id = Column(Integer, primary_key=True)
    ticker = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, default="", nullable=True)