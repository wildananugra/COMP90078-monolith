from schemas.deposit import *
from schemas.withdrawal import *
from schemas.transfer import *
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.history import HistoricalTransactionModel
from fastapi import HTTPException
from datetime import datetime, timedelta
from models.account import AccountModel
from models.card import CardModel
from models.parameter import ParameterModel
from config import Settings
import random
import string
import requests

# TODO: there is no same journal number in a day. 
def generate_journal_number(db: Session, size=6):
    journal_number = ''.join(random.choice(string.digits) for _ in range(size))
    db_journal_number = db.query(HistoricalTransactionModel).filter(and_((HistoricalTransactionModel.timestamp + timedelta(days=1)) > datetime.now(), HistoricalTransactionModel.journal_number == journal_number)).first()
    if db_journal_number:
        generate_journal_number(db)
    return journal_number

def select_account_by_account_number(db: Session, account_number: str):
    return db.query(AccountModel).filter(AccountModel.account_number == account_number).first()

def select_card_by_account_number(db: Session, account_number: str):
    return db.query(CardModel).filter(CardModel.account_number == account_number).first()

def select_parameter_by_bank_code(db: Session, bank_code: str):
    return db.query(ParameterModel).filter(and_(ParameterModel.parameter_type == "BANK_CODE", ParameterModel.key == bank_code)).first()

def deposit(db: Session, deposit: DepositSchema):

    # set initial
    journal_number = generate_journal_number(db)
    timestamp = datetime.utcnow()

    # check from account number
    current_account_number = select_account_by_account_number(db, deposit.account_number)
    if not current_account_number:
        raise HTTPException(status_code=400, detail="Acccount number doesn't exist")

    # insert historical transaction account number
    current_account_historical = HistoricalTransactionModel(
        account_number=deposit.account_number,
        transaction_type="DEPOSIT",
        action="CREDIT",
        amount=deposit.amount,
        balance=current_account_number.balance + deposit.amount,
        # timestamp=timestamp,
        journal_number=journal_number
    )
    db.add(current_account_historical)

    # update balance from account number
    setattr(current_account_number, 'balance', current_account_number.balance + deposit.amount)
            
    # commit 
    db.commit()
    
    return DepositOKSchema(
        journal_number=journal_number,
        timestamp=timestamp,
        amount=deposit.amount,
        balance=current_account_number.balance,
        account_number=deposit.account_number
    ).dict()

def withdrawal(db: Session, withdrawal: WithdrawalSchema):
    # set initial
    journal_number = generate_journal_number(db)
    timestamp = datetime.utcnow()

    # check from account number
    current_account_number = select_account_by_account_number(db, withdrawal.account_number)
    if not current_account_number:
        raise HTTPException(status_code=400, detail="Acccount number doesn't exist")

    # check id number
    if current_account_number.id_number != withdrawal.id_number:
        raise HTTPException(status_code=400, detail="ID Number invalid")

    # check sufficient fund
    if current_account_number.balance < withdrawal.amount:
        raise HTTPException(status_code=400, detail="Unsufficient fund")

    # insert historical transaction account number
    current_account_historical = HistoricalTransactionModel(
        account_number=withdrawal.account_number,
        transaction_type="WITHDRAWAL",
        action="DEBIT",
        amount=withdrawal.amount,
        balance=current_account_number.balance - withdrawal.amount,
        # timestamp=timestamp,
        journal_number=journal_number
    )
    db.add(current_account_historical)

    # update balance from account number
    setattr(current_account_number, 'balance', current_account_number.balance - withdrawal.amount)
            
    # commit 
    db.commit()
    
    return WithdrawalOKSchema(
        journal_number=journal_number,
        timestamp=timestamp,
        amount=withdrawal.amount,
        balance=current_account_number.balance,
        account_number=withdrawal.account_number,
        id_number=withdrawal.id_number
    ).dict()

def transfer(db: Session, transfer: TransferSchema):
    # set initial
    journal_number = generate_journal_number(db)
    timestamp = datetime.utcnow()

    # check from from account number
    from_current_account_number = select_account_by_account_number(db, transfer.from_account_number)
    if not from_current_account_number:
        raise HTTPException(status_code=400, detail="From Acccount number doesn't exist")

    # check from from account number
    to_current_account_number = select_account_by_account_number(db, transfer.to_account_number)
    if not to_current_account_number:
        raise HTTPException(status_code=400, detail="To Acccount number doesn't exist")

    # check sufficient fund
    if from_current_account_number.balance < transfer.amount:
        raise HTTPException(status_code=400, detail="Unsufficient fund")

    # insert historical transaction account number
    from_current_account_historical = HistoricalTransactionModel(
        account_number=transfer.from_account_number,
        transaction_type="TRANSFER",
        action="DEBIT",
        amount=transfer.amount,
        balance=from_current_account_number.balance - transfer.amount,
        journal_number=journal_number
    )
    db.add(from_current_account_historical)

    # insert historical transaction account number
    to_current_account_historical = HistoricalTransactionModel(
        account_number=transfer.to_account_number,
        transaction_type="TRANSFER",
        action="CREDIT",
        amount=transfer.amount,
        balance=to_current_account_number.balance + transfer.amount,
        journal_number=journal_number
    )
    db.add(to_current_account_historical)

    # update balance account number
    setattr(from_current_account_number, 'balance', from_current_account_number.balance - transfer.amount)
    setattr(to_current_account_number, 'balance', to_current_account_number.balance + transfer.amount)
            
    # commit 
    db.commit()
    
    return TransferOKSchema(
        journal_number=journal_number,
        timestamp=timestamp,
        amount=transfer.amount,
        balance=from_current_account_number.balance,
        from_account_number=transfer.from_account_number,
        to_account_number=transfer.to_account_number
    ).dict()

def history(db: Session, account_number: str, skip: int = 0, limit: int = 0):
    return db.query(HistoricalTransactionModel).filter(HistoricalTransactionModel.account_number == account_number).order_by(HistoricalTransactionModel.timestamp.desc()).offset(skip).limit(limit).all()

def interbank_inquiry(db: Session, interbank_inq: InterbankInquirySchema):
    db_from_account_number = select_card_by_account_number(db, interbank_inq.from_account_number)
    db_parameter = select_parameter_by_bank_code(db, interbank_inq.bank_code)

    if not db_from_account_number:
        raise HTTPException(status_code=400, detail="From Acccount number doesn't exist")
    
    if not db_parameter:
        raise HTTPException(status_code=400, detail="Bank Code doesn't exist")

    response = requests.post(f"{Settings().simulator_host}/interbank", json={}, headers={ 'Action' : 'INQUIRY' })

    return response.json()

def interbank_transfer(db: Session, interbank_trf: InterbankTransferSchema):
    journal_number = generate_journal_number(db)

    db_from_account_number = select_card_by_account_number(db, interbank_trf.from_account_number)
    db_customer_account = select_account_by_account_number(db, interbank_trf.from_account_number)

    db_parameter = select_parameter_by_bank_code(db, interbank_trf.bank_code)

    if not db_from_account_number:
        raise HTTPException(status_code=400, detail="From Acccount number doesn't exist")

    if not db_customer_account:
        raise HTTPException(status_code=400, detail="From Acccount number doesn't exist")

    if not db_parameter:
        raise HTTPException(status_code=400, detail="Bank Code doesn't exist")

    # update history transaction customer account
    db.add(HistoricalTransactionModel(
        account_number=db_from_account_number.account_number,
        transaction_type="PAYMENT",
        action="DEBIT",
        amount=interbank_trf.from_account_number,
        balance=db_customer_account.balance - int(interbank_trf.amount),
        journal_number=journal_number
    ))

    response = requests.post(f"{Settings().simulator_host}/interbank", json={}, headers={ 'Action' : 'PAYMENT' })

    return {
        'journal_number' : journal_number,
        'timestamp' : datetime.now(),
        'response_host' : response.json()
    }