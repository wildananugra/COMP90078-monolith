from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class TransferSchema(BaseModel):
    from_account_number: str
    to_account_number: str
    amount: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "from_account_number": "0115471119",
                "to_account_number": "0115471119",
                "amount": 10000
            }
        }

class TransferOKSchema(TransferSchema):
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
                "balance": 15000
            }
        }