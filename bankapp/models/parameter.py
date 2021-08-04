from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.customer import *

from database import Base

class ParameterModel(Base):
    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True, index=True)
    parameter_type = Column(String, index=True)
    key = Column(String, index=True)
    value = Column(String)
    description = Column(String)

    