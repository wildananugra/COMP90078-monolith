from typing import List, Optional
from pydantic import BaseModel

class CustomerServiceSchema(BaseModel):
    name: str
    user_id: str
    password: str

class CustomerServiceLoginSchema(BaseModel):
    user_id: str
    password: str

class CustomerServiceUpdateSchema(BaseModel):
    name: str

class CustomerServiceUpdatePasswordSchema(BaseModel):
    old_password: str
    re_password: str
    password: str
