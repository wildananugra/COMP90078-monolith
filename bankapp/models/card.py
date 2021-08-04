from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.customer import *

from database import Base

class CardModel(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, unique=True, index=True)
    account_number = Column(String, unique=True, index=True)
    cif_number = Column(String, index=True)
    card_holder_name = Column(String)
    expired_date = Column(String)
    card_type = Column(String)
    account_id = Column(Integer, ForeignKey("accounts.id"))

    accounts = relationship("AccountModel", back_populates="cards")