from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.account import *

from database import Base

class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    id_number = Column(String, unique=True, index=True)
    cif_number = Column(String, unique=True, index=True)
    customer_id = Column(String, index=True)
    name = Column(String)
    email = Column(String)
    is_active = Column(Boolean, default=True)

    accounts = relationship("AccountModel", back_populates="customers")
    merchants = relationship("MerchantModel", back_populates="customers")