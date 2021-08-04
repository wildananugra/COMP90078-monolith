from typing import List, Optional
from pydantic import BaseModel

class ParameterSchema(BaseModel):
    parameter_type: str
    key: str
    value: str
    description: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "parameter_type": "BANK_CODE",
                "key": "014",
                "value": "BANK BCA",
                "description" : "Bank BCA"
            }
        }