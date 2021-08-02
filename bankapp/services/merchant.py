from schemas.merchant import *
from sqlalchemy.orm import Session
from models.merchant import MerchantModel
from services import customer, account
from fastapi import HTTPException
import string, random

# utils
def generate_merchant_code(size=10):
    return ''.join(random.choice(string.digits) for _ in range(size))

def select_by_merchant_code(db, merchant_code):
    return db.query(MerchantModel).filter(MerchantModel.merchant_code == merchant_code).first()

# services
def create(db: Session, merchant: MerchantSchema):
    db_customer = customer.select_by_cif(db, merchant.cif_number)
    if not db_customer:
        raise HTTPException(status_code=400, detail="CIF Number doesnt exist") 

    db_account = account.select_by_account_number(db, merchant.account_number)
    if not db_account:
        raise HTTPException(status_code=400, detail="Account Number doesnt exist") 

    merchant_code = generate_merchant_code()

    db_merchant = MerchantModel(
        name=merchant.name,
        description=merchant.description,
        cif_number=merchant.cif_number,
        customer_id=db_customer.id,
        merchant_code=merchant_code,
        account_number=merchant.account_number
    )

    db.add(db_merchant)
    db.commit()
    db.refresh(db_merchant)

    return db_merchant

def all(db: Session, cif_number: str):
    db_customer = customer.select_by_cif(db, cif_number)

    if not db_customer:
        raise HTTPException(status_code=400, detail="CIF Number doesnt exist") 

    db_merchant_list = db.query(MerchantModel).filter(MerchantModel.cif_number == cif_number).all()

    return {"data" : db_merchant_list}

def detail(db: Session, merchant_code: str):
    db_merchant = select_by_merchant_code(db, merchant_code)
    if db_merchant:
        return db_merchant
    else:
        raise HTTPException(status_code=400, detail="Merchant Code doesnt exist") 

def delete(db: Session, merchant_code: str):
    db_merchant = select_by_merchant_code(db, merchant_code)
    if db_merchant:
        db.delete(db_merchant)
        db.commit()
    return db_merchant

def update(db: Session, merchant: MerchantUpdateSchema, merchant_id: int):
    db_merchant = db.query(MerchantModel).filter(MerchantModel.id == merchant_id).first()
    if not db_merchant:
        raise HTTPException(status_code=400, detail="Merchant ID doesnt exist")

    db_account = account.select_by_account_number(db, merchant.account_number)
    if not db_account:
        raise HTTPException(status_code=400, detail="Account Number doesnt exist") 
    
    setattr(db_merchant, "name", merchant.name)
    setattr(db_merchant, "description", merchant.description)
    setattr(db_merchant, "account_number", merchant.account_number)

    db.commit()

    return MerchantSchema(
        name=merchant.name,
        description=merchant.description,
        cif_number=db_merchant.cif_number,
        merchant_code=db_merchant.merchant_code,
        account_number=merchant.account_number
    ).dict()
    
