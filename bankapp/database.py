from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLALCHEMY_DATABASE_URL = os.getenv("DB_CONNECTION")
SQLALCHEMY_DATABASE_URL = "postgresql://comp90078:comp90078!@localhost/comp90078-db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()