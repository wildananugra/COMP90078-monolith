from typing import List, Optional
from pydantic import BaseModel

class CardSchema(BaseModel):
    card_number: str = None
    account_number: str
    card_holder_name: str
    expired_date: str
    card_type: str
    cif_number: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "cif_number": "0640991803",
                "account_number": "1154711190",
                "card_holder_name": "WILDAN ANUGRAH PUTRA",
                "expired_date": "05/24",
                "card_type" : "GOLD"
            }
        }

class CardUpdateSchema(BaseModel):
    card_holder_name: str
    expired_date: str
    card_type: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "card_holder_name": "WILDAN ANUGRAH PUTRA",
                "expired_date": "05/24",
                "card_type" : "GOLD"
            }
        }