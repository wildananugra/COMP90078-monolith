from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.customer import *

from database import Base

class MerchantModel(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    cif_number = Column(String, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    merchant_code = Column(String, index=True)
    account_number = Column(String, index=True)

    customers = relationship("CustomerModel", back_populates="merchants")