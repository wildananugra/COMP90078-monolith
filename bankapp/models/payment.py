from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from models.customer import *

from database import Base

class PaymentModel(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    customer_reference_id = Column(String, unique=True, index=True)
    merchant_code = Column(String, index=True)
    account_number = Column(String, index=True)
    cif_number = Column(String, index=True)
    request_raw = Column(Text)
    response_raw = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow())
