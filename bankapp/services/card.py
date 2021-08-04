from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, Request
from config import Settings
from datetime import datetime, timedelta
from schemas.card import *
from models.card import CardModel
from models.account import AccountModel
from models.customer import CustomerModel
import random, string

def generate_card_number(db: Session, size=16):
    card_number = ''.join(random.choice(string.digits) for _ in range(size))
    db_card_number = db.query(CardModel).filter(CardModel.card_number == card_number).first()
    if db_card_number:
        generate_card_number(db)
    else:
        return card_number

def select_account_by_account_number(db: Session, account_number: str):
    return db.query(AccountModel).filter(AccountModel.account_number == account_number).first()

def select_by_card_number(db: Session, card_number: str):
    return db.query(CardModel).filter(CardModel.card_number == card_number).first()

def select_by_account_number(db: Session, account_number: str):
    return db.query(CardModel).filter(CardModel.account_number == account_number).first()

def select_customer_by_cif_number(db: Session, cif_number: str):
    return db.query(CustomerModel).filter(CustomerModel.cif_number == cif_number).first()

def create(db: Session, card: CardSchema):

    card_number = generate_card_number(db)
    db_account = select_account_by_account_number(db, card.account_number)

    db_account_card = select_by_account_number(db, card.account_number)

    if db_account_card:
        raise HTTPException(status_code=400, detail="Account Number exists") 

    db_card_number = CardModel(
        card_number = card_number,
        account_number = card.account_number,
        card_holder_name = card.card_holder_name,
        expired_date = card.expired_date,
        card_type = card.card_type,
        cif_number = card.cif_number,
        account_id = db_account.id
    )

    db.add(db_card_number)
    db.commit()
    db.refresh(db_card_number)

    return db_card_number

def all(db: Session, cif_number: str):

    db_customer = select_customer_by_cif_number(db, cif_number)

    if not db_customer:
        raise HTTPException(status_code=400, detail="CIF Number doesnt exist") 
    
    return db.query(CardModel).filter(CardModel.cif_number == cif_number).all()

def detail(db: Session, card_number: str):
    db_card = select_by_card_number(db, card_number)

    if not db_card:
        raise HTTPException(status_code=400, detail="Card Number doesnt exist")

    return db_card

def update(db: Session, card: CardSchema, card_number: str):
    db_card = select_by_card_number(db, card_number)

    setattr(db_card, "card_holder_name", card.card_holder_name)
    setattr(db_card, "expired_date", card.expired_date)
    setattr(db_card, "card_type", card.card_type)

    db.commit()
    db.refresh(db_card)

    return db_card

def unlink(db: Session, card_number: str):
    db_card = select_by_card_number(db, card_number)

    if not db_card:
        raise HTTPException(status_code=400, detail="Card Number doesnt exist")
    
    setattr(db_card, "account_number", "")

    db.commit()
    db.refresh(db_card)

    return db_card

def delete(db: Session, card_number: str):
    db_card = select_by_card_number(db, card_number)
    if db_card:
        db.delete(db_card)
        db.commit()

    return { "message" : f"{card_number} has bee deleted!" }

