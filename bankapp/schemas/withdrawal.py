from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class WithdrawalSchema(BaseModel):
    account_number: str
    id_number: str
    amount: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "account_number": "0115471119",
                "amount": 10000,
                "id_number": "3175023005910005"
            }
        }

class WithdrawalOKSchema(WithdrawalSchema):
    timestamp: datetime
    journal_number: str
    balance: int
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "account_number": "0115471119",
                "amount": 10000,
                "timestamp": datetime.now(),
                "journal_number": "123456",
                "balance": 15000,
                "id_number": "3175023005910005"
            }
        }