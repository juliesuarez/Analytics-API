# Data structures (Pydantic models) for Chartify API
# models.py
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# --- INTERNAL DB SETUP (Where you store customer info) ---
Base = declarative_base()

class DataSource(Base):
    """Stores customer connection details securely."""
    __tablename__ = "data_sources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String) # e.g. "My Production DB"
    db_type = Column(String) # 'postgresql' or 'mysql'
    host = Column(String)
    port = Column(String)
    user = Column(String)
    encrypted_password = Column(String) # We store the encrypted version
    database_name = Column(String)

# Create your internal DB
db_path = os.getenv("DB_PATH", "internal.db")
db_url = f"sqlite:///{db_path}"

# Ensure the directory exists if it's in a subfolder
if "/" in db_path:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

internal_engine = create_engine(db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=internal_engine)
Base.metadata.create_all(bind=internal_engine)

# --- Pydantic Models for API Requests/Responses ---

class SourceCreate(BaseModel):
    name: str
    db_type: str
    host: str
    port: str
    user: str
    password: str
    database_name: str

class AnalyticsRequest(BaseModel):
    source_id: int
    table_name: str
    group_by_column: str
    measure_column: str
    operation: str  # sum, count, avg