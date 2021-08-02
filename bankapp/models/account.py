from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.customer import *

from database import Base

class AccountModel(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True)
    cif_number = Column(String, index=True)
    id_number = Column(String, index=True)
    balance = Column(Integer, default=0)
    currency = Column(String, default="IDR")
    customer_id = Column(Integer, ForeignKey("customers.id"))
    is_active = Column(Boolean, default=True)

    customers = relationship("CustomerModel", back_populates="accounts")