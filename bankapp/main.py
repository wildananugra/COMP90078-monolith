from typing import List
from fastapi import Depends, FastAPI, Body, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schemas.customer import *
from schemas.account import *
from schemas.deposit import *
from schemas.transfer import *
from schemas.withdrawal import *
from schemas.merchant import *
from schemas.customer_service import *
from schemas.channel_user import *
from services import customer, account, transactions, merchant, payment, purchase, customer_service, channel_user
from models.customer import CustomerModel, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

tokens = ["wildan","raika"]
async def validate_token(token: str = Depends(oauth2_scheme)):
    if token not in tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

# token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "wildan" and form_data.password == "password":
        return {"access_token": form_data.username, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

# Customers
@app.post(
    "/customer/", 
    tags=["Customers"],
)
def create_customers(
    customer_req: CustomerSchema = Body(
        ...,
        example = {
            "name" : "Customer name",
            "id_number": "3175023005910001"
        }
    ),
    db: Session = Depends(get_db),
    # token: str = Depends(validate_token)
):
    return customer.create(db, customer_req)

@app.get(
    "/customers/",
    tags=["Customers"]
)
def list_customers(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    return customer.all(db, skip, limit)

@app.get(
    "/customer/{id_number}",
    tags=["Customers"]
)
def detail_customers(
    id_number: str,
    db: Session = Depends(get_db)
):
    return customer.detail(db, id_number)

@app.put(
    "/customer/{cif_number}",
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
)
def list_accounts(
    cif_number: str, 
    db: Session = Depends(get_db)
):
    return account.all(db, cif_number)

@app.get(
    "/account/{account_number}",
    tags=["Accounts"],
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

# payment & purchase
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

# customer service
@app.get(
    "/customerservices/",
    tags=["CustomerServices"]
)
async def list_customer_services(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    return customer_service.all(db, skip, limit)

@app.get(
    "/customerservice/{user_id}",
    tags=["CustomerServices"]
)
async def detail_customer_services(
    user_id: str,
    db: Session = Depends(get_db)
):
    return customer_service.detail(db, user_id)

@app.post(
    "/customerservice/",
    tags=["CustomerServices"]
)
async def create_customer_services(
    customer_service_req: CustomerServiceSchema,
    db: Session = Depends(get_db)
):
    return customer_service.create(db, customer_service_req)

@app.post(
    "/customerservice/login/",
    tags=["CustomerServices"]
)
async def login_customer_services(
    customer_service_req: CustomerServiceLoginSchema,
    db: Session = Depends(get_db)
):
    return customer_service.login(db, customer_service_req)

@app.put(
    "/customerservice/{user_id}",
    tags=["CustomerServices"]
)
async def update_customer_services(
    customer_service_req: CustomerServiceUpdateSchema,
    user_id: str,
    db: Session = Depends(get_db)
):
    return customer_service.update(db, customer_service_req, user_id)

@app.put(
    "/customerservice/password/{user_id}",
    tags=["CustomerServices"]
)
async def update_password_customer_services(
    customer_service_req: CustomerServiceUpdatePasswordSchema,
    user_id: str,
    db: Session = Depends(get_db)
):
    return customer_service.update_password(db, customer_service_req, user_id)

@app.delete(
    "/customerservice/{user_id}",
    tags=["CustomerServices"]
)
async def delete_customer_services(
    user_id: str,
    db: Session = Depends(get_db)
):
    return customer_service.delete(db, user_id)

#channel ibank
@app.get(
    "/channel/ibank",
    tags=["ChannelIBank"]
)
async def list_ibank_user(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    return channel_user.all(db, "IBANK", skip, limit)

@app.get(
    "/channel/ibank/{user_id}",
    tags=["ChannelIBank"]
)
async def detail_ibank_user(
    user_id: str, 
    db: Session = Depends(get_db)
):
    return channel_user.detail(db, user_id, "IBANK")

@app.post(
    "/channel/ibank/",
    tags=["ChannelIBank"]
)
async def create_ibank_user(
    channel_user_req: ChannelUserSchema,
    db: Session = Depends(get_db)
):
    return channel_user.create(db, channel_user_req, "IBANK")

@app.post(
    "/channel/ibank/login/",
    tags=["ChannelIBank"]
)
async def login_ibank_user(
    channel_user_req: ChannelUserLoginSchema,
    db: Session = Depends(get_db)
):
    return channel_user.login(db, channel_user_req, "IBANK")

@app.put(
    "/channel/ibank/{user_id}",
    tags=["ChannelIBank"]
)
async def update_ibank_user(
    channel_user_req: ChannelUserUpdateSchema,
    user_id: str, 
    db: Session = Depends(get_db)
):
    return channel_user.update(db, channel_user_req, user_id, "IBANK")

@app.put(
    "/channel/ibank/password/{user_id}",
    tags=["ChannelIBank"]
)
async def update_password_ibank_user(
    channel_user_req: ChannelUserUpdatePasswordSchema,
    user_id: str, 
    db: Session = Depends(get_db)
):
    return channel_user.update_password(db, channel_user_req, user_id, "IBANK")

@app.delete(
    "/channel/ibank/{user_id}",
    tags=["ChannelIBank"]
)
async def delete_customer_services(
    user_id: str, 
    db: Session = Depends(get_db)
):
    return channel_user.delete(db, user_id, "IBANK")

#channel mbank
@app.get(
    "/channel/mbank/",
    tags=["ChannelMbank"]
)
async def list_mbank_user(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    return channel_user.all(db, "MBANK", skip, limit)

@app.get(
    "/channel/mbank/{user_id}",
    tags=["ChannelMbank"]
)
async def detail_mbank_user(
    user_id: str, 
    db: Session = Depends(get_db)
):
    return channel_user.detail(db, user_id, "MBANK")

@app.post(
    "/channel/mbank/",
    tags=["ChannelMbank"]
)
async def create_mbank_user(
    channel_user_req: ChannelUserSchema,
    db: Session = Depends(get_db)
):
    return channel_user.create(db, channel_user_req, "MBANK")

@app.post(
    "/channel/mbank/login/",
    tags=["ChannelMbank"]
)
async def login_mbank_user(
    channel_user_req: ChannelUserLoginSchema,
    db: Session = Depends(get_db)
):
    return channel_user.login(db, channel_user_req, "MBANK")

@app.put(
    "/channel/mbank/",
    tags=["ChannelMbank"]
)
async def update_mbank_user(
    channel_user_req: ChannelUserUpdateSchema,
    user_id: str, 
    db: Session = Depends(get_db)
):
    return channel_user.update(db, channel_user_req, user_id, "MBANK")

@app.put(
    "/channel/mbank/password/{user_id}",
    tags=["ChannelMbank"]
)
async def update_password_mbank_user(
    channel_user_req: ChannelUserUpdatePasswordSchema,
    user_id: str, 
    db: Session = Depends(get_db)
):
    return channel_user.update_password(db, channel_user_req, user_id, "MBANK")

@app.delete(
    "/channel/mbank/{user_id}",
    tags=["ChannelMbank"]
)
async def delete_customer_services(
    user_id: str, 
    db: Session = Depends(get_db)
):
    return channel_user.delete(db, user_id, "MBANK")