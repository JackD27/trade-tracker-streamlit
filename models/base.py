import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
os.makedirs(base_dir, exist_ok=True)
db_path = os.path.join(base_dir, "portfolio.db")

Base = declarative_base()
engine = create_engine(f"sqlite:///{db_path}", echo=False)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
