from schemas.deposit import *
from schemas.withdrawal import *
from schemas.transfer import *
from sqlalchemy.orm import Session
from models.history import HistoricalTransactionModel
from fastapi import HTTPException
from services import account
from datetime import datetime
import random
import string

# TODO: there is no same journal number in a day. 
def generate_journal_number(size=6):
    return ''.join(random.choice(string.digits) for _ in range(size))

def deposit(db: Session, deposit: DepositSchema):

    # set initial
    journal_number = generate_journal_number()
    timestamp = datetime.utcnow()

    # check from account number
    current_account_number = account.select_by_account_number(db, deposit.account_number)
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
    journal_number = generate_journal_number()
    timestamp = datetime.utcnow()

    # check from account number
    current_account_number = account.select_by_account_number(db, withdrawal.account_number)
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
    journal_number = generate_journal_number()
    timestamp = datetime.utcnow()

    # check from from account number
    from_current_account_number = account.select_by_account_number(db, transfer.from_account_number)
    if not from_current_account_number:
        raise HTTPException(status_code=400, detail="From Acccount number doesn't exist")

    # check from from account number
    to_current_account_number = account.select_by_account_number(db, transfer.to_account_number)
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