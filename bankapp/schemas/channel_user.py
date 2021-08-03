from typing import List, Optional
from pydantic import BaseModel

class ChannelUserSchema(BaseModel):
    id_number: str
    name: str
    user_id: str
    password: str

class ChannelUserLoginSchema(BaseModel):
    user_id: str
    password: str

class ChannelUserUpdateSchema(BaseModel):
    name: str

class ChannelUserUpdatePasswordSchema(BaseModel):
    old_password: str
    re_password: str
    password: str
