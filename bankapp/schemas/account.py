from typing import List, Optional
from pydantic import BaseModel

class AccountSchema(BaseModel):
    id_number: str
    account_number: Optional[str] = None
    cif_number: str = None
    balance: int = None
    currency: str = None
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_number": "3175023005910005",
                "account_number": "0115471119",
                "balance": 1000,
                "cif_number": "9001230101",
                "currency": "IDR"
            }
        }
class AccountListSchema(BaseModel):
    data: List[AccountSchema]