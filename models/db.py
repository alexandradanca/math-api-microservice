from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///data/requests.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MathRequestDB(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, index=True)
    input_data = Column(String)
    result = Column(Float)
