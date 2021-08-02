from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class MerchantSchema(BaseModel):
    
    name: str
    description: str
    account_number: str
    cif_number: str
    merchant_code: str = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "merchant name",
                "description": "merchant description",
                "cif_number": "9065166200",
                "account_number": "115471119"
            }
        }

class MerchantUpdateSchema(BaseModel):
    
    name: str
    account_number: str
    description: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "merchant name",
                "description": "merchant description",
                "account_number": "115471119"
            }
        }

class MerchantAccountSchema(BaseModel):
    
    account_number: str
    merchant_name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "account_number": "115471119",
                "merchant_name": "Merchant Name"
            }
        }

class MerchantAccountListSchema(BaseModel):
    
    data: List[MerchantSchema]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "data" : [
                    {
                        "account_number": "115471119",
                        "merchant_name": "merchant name 1"
                    },
                    {
                        "account_number": "115471120",
                        "merchant_name": "merchant name 2"
                    },
                    {
                        "account_number": "115471121",
                        "merchant_name": "merchant name 3"
                    }
                ]
            }
        }