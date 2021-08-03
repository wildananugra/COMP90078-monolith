from sqlalchemy.orm import Session
from models.merchant import MerchantModel
from models.history import HistoricalTransactionModel
from fastapi import HTTPException, Request
from models.h2h_lookup import H2HLookupModel
from config import Settings
from datetime import datetime
import json
import requests
import random, string

# utils
def generate_journal_number(db: Session, size=6):
    journal_number = ''.join(random.choice(string.digits) for _ in range(size))
    db_journal_number = db.query(HistoricalTransactionModel).filter(and_((HistoricalTransactionModel.timstamp + timedelta(days=1)) > datetime.now(), HistoricalTransactionModel.journal_number == journal_number)).first()
    if db_journal_number:
        generate_journal_number(db)
    return journal_number

def generate_customer_reference_id(db: Session, size=10):
    customer_reference_id = ''.join(random.choice(string.digits) for _ in range(size))
    db_customer_reference_id = db.query(H2HLookupModel).filter(H2HLookupModel.customer_reference_id == customer_reference_id).first()
    if db_customer_reference_id:
        generate_customer_reference_id(db)
    return db_customer_reference_id

def select_merchant_by_merchant_code(db: Session, merchant_code: str):
    return db.query(MerchantModel).filter(MerchantModel.merchant_code == merchant_code).first()

def select_account_by_account_number(db: Session, account_number: str):
    return db.query(AccountModel).filter(AccountModel.account_number == account_number).first()

# main 
def merchant_one_inquiry(db: Session, request: Request):
    return requests.post(f"{Settings().simulator_host}/merchant-1", json={}, headers={ 'Action' : 'INQUIRY' })

def merchant_one_payment(db: Session, request: Request):
    return requests.post(f"{Settings().simulator_host}/merchant-1", json={}, headers={ 'Action' : 'PAYMENT' })

# inquiry
async def inq(db: Session, request: Request):
    merchant_code = request.path_params['merchant_code']
    db_merchant = select_merchant_by_merchant_code(db, merchant_code)

    response = {}
    if not db_merchant:
        raise HTTPException(status_code=400, detail="Merchant Code doesnt exist") 
    else:
        request_body = await request.json()
        if merchant_code == "4958964369":
            response = merchant_one_inquiry(db, request)

            status_code = response.status_code
            response_text = json.dumps(response.json())
            request_text = json.dumps(request_body)

            db.add(H2HLookupModel(
                customer_reference_id=generate_customer_reference_id(),
                merchant_code=merchant_code,
                action="INQUIRY",
                status=status_code,
                request_raw=request_text,
                response_raw=response_text,
                transaction_type="PURCHASE"
            ))

            db.commit()

        else:
            return { "message" : "invalid merchant code." }

    return response.json()

# payment
async def pay(db: Session, request: Request):
    merchant_code = request.path_params['merchant_code']
    db_merchant = select_merchant_by_merchant_code(db, merchant_code)
    journal_number = generate_journal_number()
    customer_reference_id = generate_customer_reference_id()

    response = {}
    if not db_merchant:
        raise HTTPException(status_code=400, detail="Merchant Code doesnt exist") 
    else:
        request_body = await request.json()
        customer_account = request_body['account']
        
        # validate debit account
        db_customer_account = select_account_by_account_number(db, customer_account)
        if not db_customer_account:
            raise HTTPException(status_code=400, detail="Customer account doesnt exist") 
        
        # validate debit account
        db_merchant_account = select_account_by_account_number(db, db_merchant.account_number)
        if not db_merchant_account:
            raise HTTPException(status_code=400, detail="Merchant account doesnt exist") 

        # validate customer account balance
        if db_customer_account.balance < int(request_body['amount']):
            raise HTTPException(status_code=400, detail="Unsufficient fund") 

        # update history transaction customer account
        db.add(HistoricalTransactionModel(
            account_number=db_customer_account.account_number,
            transaction_type="PURCHASE",
            action="DEBIT",
            amount=request_body['amount'],
            balance=db_customer_account.balance - int(request_body['amount']),
            journal_number=journal_number
        ))

        # update history transaction merchant account
        db.add(HistoricalTransactionModel(
            account_number=db_merchant_account.account_number,
            transaction_type="PURCHASE",
            action="CREDIT",
            amount=request_body['amount'],
            balance=db_merchant_account.balance + int(request_body['amount']),
            journal_number=journal_number
        ))

        # update balance debit account
        setattr(db_merchant_account, 'balance', db_merchant_account.balance + int(request_body['amount']))

        # update balance merchant account
        setattr(db_customer_account, 'balance', db_customer_account.balance - int(request_body['amount']))

        if merchant_code == "4958964369":
            response = merchant_one_payment(db, request)

            status_code = response.status_code
            response_text = json.dumps(response.json())
            request_text = json.dumps(request_body)

            db.add(H2HLookupModel(
                customer_reference_id=customer_reference_id,
                merchant_code=merchant_code,
                action="PAYMENT",
                status=status_code,
                request_raw=request_text,
                response_raw=response_text,
                account_number=db_customer_account.account_number,
                cif_number=db_customer_account.cif_number,
                transaction_type="PURCHASE"
            ))

        else:
            db.rollback()
            return { "message" : "invalid merchant code." }

        db.commit()

    return {
        'journal_number' : journal_number,
        'customer_reference_id': customer_reference_id,
        'timestamp' : datetime.now(),
        'data' : response.json()
    }