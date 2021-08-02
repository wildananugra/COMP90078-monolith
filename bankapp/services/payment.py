from sqlalchemy.orm import Session
from models.merchant import MerchantModel
from models.history import HistoricalTransactionModel
from services import customer, merchant, account
from fastapi import HTTPException, Request
from config import Settings
import json
import requests
import random, string

# utils
def generate_journal_number(size=6):
    return ''.join(random.choice(string.digits) for _ in range(size))

# main 
def merchant_one_inquiry(db: Session, request: Request):
    return requests.post(f"{Settings().simulator_host}/merchant-1", json={}, headers={ 'Action' : 'INQUIRY' }).json()

def merchant_one_payment(db: Session, request: Request):
    return requests.post(f"{Settings().simulator_host}/merchant-1", json={}, headers={ 'Action' : 'PAYMENT' }).json()

# inquiry
async def inq(db: Session, request: Request):
    merchant_code = request.path_params['merchant_code']
    db_merchant = merchant.select_by_merchant_code(db, merchant_code)

    response = {}
    if not db_merchant:
        raise HTTPException(status_code=400, detail="Merchant Code doesnt exist") 
    else:
        request_body = await request.json()
        if merchant_code == "4958964369":
            response = merchant_one_inquiry(db, request)
        else:
            response = { "message" : "invalid merchant code." }

    return response

# payment
async def pay(db: Session, request: Request):
    merchant_code = request.path_params['merchant_code']
    db_merchant = merchant.select_by_merchant_code(db, merchant_code)
    journal_number = generate_journal_number()

    response = {}
    if not db_merchant:
        raise HTTPException(status_code=400, detail="Merchant Code doesnt exist") 
    else:
        request_body = await request.json()
        customer_account = request_body['account']
        
        # validate debit account
        db_customer_account = account.select_by_account_number(db, customer_account)
        if not db_customer_account:
            raise HTTPException(status_code=400, detail="Customer account doesnt exist") 
        
        # validate debit account
        db_merchant_account = account.select_by_account_number(db, db_merchant.account_number)
        if not db_merchant_account:
            raise HTTPException(status_code=400, detail="Merchant account doesnt exist") 

        # validate customer account balance
        if db_customer_account.balance < int(request_body['amount']):
            raise HTTPException(status_code=400, detail="Unsufficient fund") 

        # update history transaction customer account
        db.add(HistoricalTransactionModel(
            account_number=db_customer_account.account_number,
            transaction_type="PAYMENT",
            action="DEBIT",
            amount=request_body['amount'],
            balance=db_customer_account.balance - int(request_body['amount']),
            journal_number=journal_number
        ))

        # update history transaction merchant account
        db.add(HistoricalTransactionModel(
            account_number=db_merchant_account.account_number,
            transaction_type="PAYMENT",
            action="CREDIT",
            amount=request_body['amount'],
            balance=db_merchant_account.balance + int(request_body['amount']),
            journal_number=journal_number
        ))

        # update balance debit account
        setattr(db_merchant_account, 'balance', db_merchant_account.balance + int(request_body['amount']))

        # update balance merchant account
        setattr(db_customer_account, 'balance', db_customer_account.balance - int(request_body['amount']))

        db.commit()

        if merchant_code == "4958964369":
            response = merchant_one_payment(db, request)
        else:
            response = { "message" : "invalid merchant code." }

    return response