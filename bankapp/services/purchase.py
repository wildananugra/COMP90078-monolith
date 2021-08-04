from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.merchant import MerchantModel
from models.history import HistoricalTransactionModel
from models.account import AccountModel
from fastapi import HTTPException, Request
from models.h2h_lookup import H2HLookupModel
from config import Settings
from datetime import datetime, timedelta
import json
import requests
import random, string

# utils
def generate_journal_number(db: Session, size=6):
    journal_number = ''.join(random.choice(string.digits) for _ in range(size))
    db_journal_number = db.query(HistoricalTransactionModel).filter(and_((HistoricalTransactionModel.timestamp + timedelta(days=1)) > datetime.now(), HistoricalTransactionModel.journal_number == journal_number)).first()
    if db_journal_number:
        generate_journal_number(db)
    return journal_number

def generate_customer_reference_id(db: Session, size=10):
    customer_reference_id = ''.join(random.choice(string.digits) for _ in range(size))
    db_customer_reference_id = db.query(H2HLookupModel).filter(H2HLookupModel.customer_reference_id == customer_reference_id).first()
    if db_customer_reference_id:
        generate_customer_reference_id(db)
    return customer_reference_id

def select_merchant_by_merchant_code(db: Session, merchant_code: str):
    return db.query(MerchantModel).filter(MerchantModel.merchant_code == merchant_code).first()

def select_account_by_account_number(db: Session, account_number: str):
    return db.query(AccountModel).filter(AccountModel.account_number == account_number).first()

# main 
def creditcard(db: Session, request: Request, action: str):
    return requests.post(f"{Settings().simulator_host}/creditcard", json={}, headers={ 'Action' : action })

def ecommerce(db: Session, request: Request, action: str):
    return requests.post(f"{Settings().simulator_host}/ecommerce", json={}, headers={ 'Action' : action })

def education(db: Session, request: Request, action: str):
    return requests.post(f"{Settings().simulator_host}/education", json={}, headers={ 'Action' : action })

def electrical(db: Session, request: Request, action: str):
    return requests.post(f"{Settings().simulator_host}/electrical", json={}, headers={ 'Action' : action })

def emoney(db: Session, request: Request, action: str):
    return requests.post(f"{Settings().simulator_host}/emoney", json={}, headers={ 'Action' : action })

def flight(db: Session, request: Request, action: str):
    return requests.post(f"{Settings().simulator_host}/flight", json={}, headers={ 'Action' : action })

def insurance(db: Session, request: Request, action: str):
    return requests.post(f"{Settings().simulator_host}/insurance", json={}, headers={ 'Action' : action })

def internetquota(db: Session, request: Request, action: str):
    return requests.post(f"{Settings().simulator_host}/internetquota", json={}, headers={ 'Action' : action })

def multifinance(db: Session, request: Request, action: str):
    return requests.post(f"{Settings().simulator_host}/multifinance", json={}, headers={ 'Action' : action })

def tax(db: Session, request: Request, action: str):
    return requests.post(f"{Settings().simulator_host}/tax", json={}, headers={ 'Action' : action })

def train(db: Session, request: Request, action: str):
    return requests.post(f"{Settings().simulator_host}/train", json={}, headers={ 'Action' : action })

def water(db: Session, request: Request, action: str):
    return requests.post(f"{Settings().simulator_host}/water", json={}, headers={ 'Action' : action })

def insert_to_db(db: Session, response, request_body, merchant_code):
    status_code = response.status_code
    response_text = json.dumps(response.json())
    request_text = json.dumps(request_body)

    db.add(H2HLookupModel(
        customer_reference_id=generate_customer_reference_id(db),
        merchant_code=merchant_code,
        action="INQUIRY",
        status=status_code,
        request_raw=request_text,
        response_raw=response_text,
        transaction_type="PAYMENT"
    ))

    return db

def insert_to_db_pay(db: Session, db_customer_account, customer_reference_id, response, request_body, merchant_code):
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
        transaction_type="PAYMENT"
    ))

    return db

# inquiry
async def inq(db: Session, request: Request):
    merchant_code = request.path_params['merchant_code']
    db_merchant = select_merchant_by_merchant_code(db, merchant_code)

    response = {}
    if not db_merchant:
        raise HTTPException(status_code=400, detail="Merchant Code doesnt exist") 
    else:
        request_body = await request.json()
        if merchant_code == "8498714638":
            response = creditcard(db, request, "INQUIRY")
            db = insert_to_db(db, response, request_body, merchant_code)
        elif merchant_code == "2781646620":
            response = ecommerce(db, request, "INQUIRY")
            db = insert_to_db(db, response, request_body, merchant_code)
        elif merchant_code == "8927603807":
            response = education(db, request, "INQUIRY")
            db = insert_to_db(db, response, request_body, merchant_code)
        elif merchant_code == "1230274831":
            response = electrical(db, request, "INQUIRY")
            db = insert_to_db(db, response, request_body, merchant_code)
        elif merchant_code == "3013612880":
            response = emoney(db, request, "INQUIRY")
            db = insert_to_db(db, response, request_body, merchant_code)
        elif merchant_code == "0694367766":
            response = flight(db, request, "INQUIRY")
            db = insert_to_db(db, response, request_body, merchant_code)
        elif merchant_code == "3925387250":
            response = insurance(db, request, "INQUIRY")
            db = insert_to_db(db, response, request_body, merchant_code)
        elif merchant_code == "2120727544":
            response = multifinance(db, request, "INQUIRY")
            db = insert_to_db(db, response, request_body, merchant_code)
        elif merchant_code == "3504254400":
            response = tax(db, request, "INQUIRY")
            db = insert_to_db(db, response, request_body, merchant_code)
        elif merchant_code == "9354275485":
            response = train(db, request, "INQUIRY")
            db = insert_to_db(db, response, request_body, merchant_code)
        elif merchant_code == "2781646620":
            response = creditcard(db, request, "INQUIRY")
            db = insert_to_db(db, response, request_body, merchant_code)
        elif merchant_code == "8357614070":
            response = water(db, request, "INQUIRY")
            db = insert_to_db(db, response, request_body, merchant_code)
        else:
            response = { "message" : "invalid merchant code." }
        db.commit()
    return response.json()

# payment
async def pay(db: Session, request: Request):
    merchant_code = request.path_params['merchant_code']
    db_merchant = select_merchant_by_merchant_code(db, merchant_code)
    journal_number = generate_journal_number(db)
    customer_reference_id = generate_customer_reference_id(db)

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

        request_body = await request.json()
        if merchant_code == "8498714638":
            response = creditcard(db, request, "PAYMENT")
            db = insert_to_db_pay(db, db_customer_account, customer_reference_id, response, request_body, merchant_code)
        elif merchant_code == "2781646620":
            response = ecommerce(db, request, "PAYMENT")
            db = insert_to_db_pay(db, db_customer_account, customer_reference_id, response, request_body, merchant_code)
        elif merchant_code == "8927603807":
            response = education(db, request, "PAYMENT")
            db = insert_to_db_pay(db, db_customer_account, customer_reference_id, response, request_body, merchant_code)
        elif merchant_code == "1230274831":
            response = electrical(db, request, "PAYMENT")
            db = insert_to_db_pay(db, db_customer_account, customer_reference_id, response, request_body, merchant_code)
        elif merchant_code == "3013612880":
            response = emoney(db, request, "PAYMENT")
            db = insert_to_db_pay(db, db_customer_account, customer_reference_id, response, request_body, merchant_code)
        elif merchant_code == "0694367766":
            response = flight(db, request, "PAYMENT")
            db = insert_to_db_pay(db, db_customer_account, customer_reference_id, response, request_body, merchant_code)
        elif merchant_code == "3925387250":
            response = insurance(db, request, "PAYMENT")
            db = insert_to_db_pay(db, db_customer_account, customer_reference_id, response, request_body, merchant_code)
        elif merchant_code == "2120727544":
            response = multifinance(db, request, "PAYMENT")
            db = insert_to_db_pay(db, db_customer_account, customer_reference_id, response, request_body, merchant_code)
        elif merchant_code == "3504254400":
            response = tax(db, request, "PAYMENT")
            db = insert_to_db_pay(db, db_customer_account, customer_reference_id, response, request_body, merchant_code)
        elif merchant_code == "9354275485":
            response = train(db, request, "PAYMENT")
            db = insert_to_db_pay(db, db_customer_account, customer_reference_id, response, request_body, merchant_code)
        elif merchant_code == "2781646620":
            response = creditcard(db, request, "PAYMENT")
            db = insert_to_db_pay(db, db_customer_account, customer_reference_id, response, request_body, merchant_code)
        elif merchant_code == "8357614070":
            response = water(db, request, "PAYMENT")
            db = insert_to_db_pay(db, db_customer_account, customer_reference_id, response, request_body, merchant_code)
        else:
            response = { "message" : "invalid merchant code." }

        db.commit()

    return {
        'journal_number' : journal_number,
        'customer_reference_id': customer_reference_id,
        'timestamp' : datetime.now(),
        'data' : response.json()
    }