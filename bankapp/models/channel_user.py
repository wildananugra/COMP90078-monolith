from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class ChannelUserModel(Base):
    __tablename__ = "channel_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    password = Column(String)
    name = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    channel_type = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    customers = relationship("CustomerModel", back_populates="channel_users")