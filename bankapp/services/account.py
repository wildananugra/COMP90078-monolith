from schemas.account import *
from sqlalchemy.orm import Session
from models.account import AccountModel
from models.customer import CustomerModel
from fastapi import HTTPException

import random
import string

# utils
def generate_account_number(db: Session, size=10):
    account_number = ''.join(random.choice(string.digits) for _ in range(size))

    if select_by_account_number(db, account_number):
        return generate_account_number(db)
    else:
        return account_number

def select_by_account_number(db: Session, account_number: str):
    return db.query(AccountModel).filter(AccountModel.account_number == account_number).first()

def select_customer_by_id_number(db: Session, id_number: str):
    return db.query(CustomerModel).filter(CustomerModel.id_number == id_number).first()

def select_customer_by_cif(db: Session, cif_number: str):
    return db.query(CustomerModel).filter(CustomerModel.cif_number == cif_number).first()

def insert_to_db(db: Session(), account):
    db_account = AccountModel(
        account_number = account['account_number'],
        cif_number = account['cif_number'],
        customer_id = account['customer_id'],
        id_number = account['id_number'],
        account_type = account['account_type']
        ) 
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

# services
def create(db: Session, account: AccountSchema):
    
    db_cust = select_customer_by_id_number(db, account.id_number)

    if db_cust:
        account_dict = account.dict()
        account_dict['cif_number'] = db_cust.cif_number
        account_dict['customer_id'] = db_cust.id
        account_dict['id_number'] = account.id_number
    else:
        raise HTTPException(status_code=400, detail="ID Number doesn't exist")

    if account.account_number:

        if len(account.account_number) != 10:
            raise HTTPException(status_code=400, detail="Account Number len should be 10")

        account_exist = select_by_account_number(db, account_number=account.account_number)
        if account_exist:
            raise HTTPException(status_code=400, detail="Account number exists")
        else:
            account_dict['account_number'] = account.account_number
            return insert_to_db(db, account_dict)
    else:
        account_number = generate_account_number(db)
        account_dict['account_number'] = account_number
        return insert_to_db(db, account_dict)

def all(db: Session, cif_number: str):
    db_cust = select_customer_by_cif(db, cif_number)
    if db_cust:
        return {"data" : db.query(AccountModel).filter(AccountModel.cif_number == cif_number).all()}
    else:
        raise HTTPException(status_code=400, detail="CIF Number doesn't exist")
    
def delete(db: Session, account_number: str):
    account = select_by_account_number(db, account_number)
    if account:
        db.delete(account)
        db.commit()
    return account

def detail(db: Session, account_number: str):
    db_account = select_by_account_number(db, account_number)
    if db_account:
        return { "data" : db_account, "customer_info" : db_account.customers }
    else:
        raise HTTPException(status_code=400, detail="Account Number doesn't exist")