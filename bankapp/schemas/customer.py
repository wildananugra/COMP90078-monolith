from typing import List, Optional
from pydantic import BaseModel

class CustomerSchema(BaseModel):
    name: str
    id_number: str
    email: Optional[str] = None

class CustomerCreateSchema(CustomerSchema):
    cif_number: str

class CustomerResponseScheme(CustomerCreateSchema):
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Customer Name",
                "id_number": "3175023005910005",
                "cif_number": "9005024001"
            }
        }

class CustomerResponseListScheme(BaseModel):
    data: List[CustomerCreateSchema]
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "data" : [
                    {
                        "name": "Customer Name 1",
                        "id_number": "3175023005910005",
                        "cif_number": "9005024001"
                    },
                    {
                        "name": "Customer Name 2",
                        "id_number": "3175023005910006",
                        "cif_number": "9005024002"
                    },
                    {
                        "name": "Customer Name 3",
                        "id_number": "3175023005910007",
                        "cif_number": "9005024003"
                    }
                ]
            }
        }
    

