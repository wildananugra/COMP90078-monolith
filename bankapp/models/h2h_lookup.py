from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from models.customer import *
from datetime import datetime

from database import Base

class H2HLookupModel(Base):
    __tablename__ = "h2h_lookups"

    id = Column(Integer, primary_key=True, index=True)
    customer_reference_id = Column(String, unique=True, index=True)
    merchant_code = Column(String, index=True)
    transaction_type = Column(String, index=True)
    account_number = Column(String, index=True, default="")
    cif_number = Column(String, index=True, default="")
    action = Column(String, index=True)
    status = Column(String, index=True)
    request_raw = Column(Text,default="")
    response_raw = Column(Text,default="")
    timestamp = Column(DateTime, default=datetime.utcnow())
