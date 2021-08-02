from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from models.account import *
from datetime import datetime

from database import Base

class HistoricalTransactionModel(Base):
    __tablename__ = "historical_transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, index=True)
    transaction_type = Column(String, index=True)
    action = Column(String, index=True)
    amount = Column(Integer)
    balance = Column(Integer)
    journal_number = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow())
