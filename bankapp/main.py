from typing import List
from fastapi import Depends, FastAPI, Body, Request
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schemas.customer import *
from schemas.account import *
from schemas.deposit import *
from schemas.transfer import *
from schemas.withdrawal import *
from schemas.merchant import *
from services import customer, account, transactions, merchant, payment, purchase
from models.customer import CustomerModel, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Customers
@app.post(
    "/customer/", 
    response_model=CustomerCreateSchema,
    tags=["Customers"]
)
def create_customers(
    customer_req: CustomerSchema = Body(
        ...,
        example = {
            "name" : "Customer name",
            "id_number": "3175023005910001"
        }
    ),
    db: Session = Depends(get_db)
):
    return customer.create(db, customer_req)

@app.get(
    "/customers/",
    response_model=CustomerResponseListScheme,
    tags=["Customers"]
)
def list_customers(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    return customer.all(db, skip, limit)

@app.get(
    "/customer/{id_number}",
    response_model=CustomerCreateSchema,
    tags=["Customers"]
)
def detail_customers(
    id_number: str,
    db: Session = Depends(get_db)
):
    return customer.detail(db, id_number)

@app.put(
    "/customer/",
    tags=["Customers"]
)
def update_customers(
    cif_number: str, 
    customer_req: CustomerSchema = Body(...,
        example = {
            "name" : "Customer name",
            "id_number": "3175023005910001",
            "email": "customer@server.com"
        }
    ),
    db: Session = Depends(get_db)
):
    return customer.update(db, customer_req, cif_number)

@app.delete(
    "/customer/{cif_number}",
    tags=["Customers"]
)
def delete_customers(
    cif_number: str, 
    db: Session = Depends(get_db)
):
    return customer.delete(db, cif_number)

# Accounts
@app.post(
    "/account/",
    tags=["Accounts"],
    response_model=AccountSchema,
)
def create_accounts(
    account_req: AccountSchema = Body(
        ...,
        example = {
            "id_number" : "3175023005910005",
            "account_number": "115471119"
        }
    ),
    db: Session = Depends(get_db)
):
    return account.create(db, account_req)

@app.get(
    "/accounts/{cif_number}",
    tags=["Accounts"],
    response_model=AccountListSchema
)
def list_accounts(
    cif_number: str, 
    db: Session = Depends(get_db)
):
    return account.all(db, cif_number)

@app.get(
    "/account/{account_number}",
    tags=["Accounts"],
    response_model=AccountSchema
)
def detail_account(
    account_number: str, 
    db: Session = Depends(get_db)
):
    return account.detail(db, account_number)

@app.delete(
    "/account/{account_number}",
    tags=["Accounts"]
)
def delete_accounts(
    account_number: str,
    db: Session = Depends(get_db)
):
    return account.delete(db, account_number)

# merchant
@app.get(
    "/merchants/{cif_number}",
    tags=["Merchants"],
    response_model=MerchantAccountListSchema
)
def list_merchants(
    cif_number: str,
    db: Session = Depends(get_db)
):
    return merchant.all(db, cif_number)

@app.get(
    "/merchant/{merchant_code}",
    tags=["Merchants"]
)
def detail_merchant(
    merchant_code: str,
    db: Session = Depends(get_db)
):
    return merchant.detail(db, merchant_code)

@app.post(
    "/merchant/",
    tags=["Merchants"]
)
def create_merchant(
    merchant_req: MerchantSchema = Body(
        ...,
        example = {
            "name" : "Merchant Name",
            "description": "Merchant description",
            "cif_number": "9065166200",
            "account_number": "115471119"
        }
    ),
    db: Session = Depends(get_db)
):
    return merchant.create(db, merchant_req)

@app.put(
    "/merchant/{merchant_id}",
    tags=["Merchants"]
)
def update_merchant(
    merchant_id: str,
    merchant_req: MerchantUpdateSchema = Body(
        ...,
        example = {
            "name" : "Merchant Name",
            "description": "Merchant description",
            "account_number": "115471119"
        }
    ),
    db: Session = Depends(get_db)
):
    return merchant.update(db, merchant_req, merchant_id)

@app.delete(
    "/merchant/{merchant_code}",
    tags=["Merchants"]
)
def delete_merchant(
    merchant_code: str,
    db: Session = Depends(get_db)
):
    return merchant.delete(db, merchant_code)

# transactions
@app.post(
    "/deposit/",
    tags=["Transactions"]
)
def deposit_trx(
    deposit: DepositSchema,
    db: Session = Depends(get_db)
):
    return transactions.deposit(db, deposit)

@app.post(
    "/withdrawal/",
    tags=["Transactions"]
)
def withdrawal(
    withdrawal: WithdrawalSchema,
    db: Session = Depends(get_db)
):
    return transactions.withdrawal(db, withdrawal)

@app.post(
    "/transfer/",
    tags=["Transactions"]
)
def transfer(
    transfer: TransferSchema,
    db: Session = Depends(get_db)
):
    return transactions.transfer(db, transfer)

@app.get(
    "/historical_transaction/{account_number}",
    tags=["Transactions"]
)
def historical_transaction(
    account_number: str,
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    return transactions.history(db, account_number, skip, limit)

@app.get(
    "/payment/{merchant_code}",
    tags=["Transactions"]
)
async def payment_inquiry(
    request: Request, 
    db: Session = Depends(get_db)
):
    return await payment.inq(db, request)

@app.post(
    "/payment/{merchant_code}",
    tags=["Transactions"]
)
async def payment_pay(
    request: Request, 
    db: Session = Depends(get_db)
):
    return await payment.pay(db, request)

@app.get(
    "/purchase/{merchant_code}",
    tags=["Transactions"]
)
async def purchased_inquiry(
    request: Request,
    db: Session = Depends(get_db)
):
    return await purchase.inq(db, request)

@app.post(
    "/purchase/{merchant_code}",
    tags=["Transactions"]
)
async def purchased_pay(
    request: Request,
    db: Session = Depends(get_db)
):
    return await purchase.pay(db, request)