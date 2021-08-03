from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.account import *

from database import Base

class CustomerServiceModel(Base):
    __tablename__ = "customer_services"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String, index=True)
    is_active = Column(Boolean, default=True)