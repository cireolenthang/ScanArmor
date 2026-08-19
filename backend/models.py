from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./smb_shield.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Scan(Base):
    __tablename__ = "scans"
    id = Column(String, primary_key=True, index=True)
    target = Column(String, index=True)
    status = Column(String, default="pending")
    results = Column(Text, default="{}")

    # SQLAlchemy stores string; helpers can serialize/deserialize
    def set_results(self, obj):
        self.results = json.dumps(obj)

    def get_results(self):
        try:
            return json.loads(self.results or "{}")
        except Exception:
            return {}

def init_db():
    Base.metadata.create_all(bind=engine)
