from schemas.channel_user import *
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.channel_user import ChannelUserModel
from models.customer import CustomerModel
from fastapi import HTTPException

# utils

def select_by_user_id(db: Session, user_id: str, channel_type: str):
    return db.query(ChannelUserModel).filter(and_(ChannelUserModel.user_id == user_id, ChannelUserModel.channel_type == channel_type)).first()

def select_customer_by_id_number(db: Session, id_number: str):
    return db.query(CustomerModel).filter(CustomerModel.id_number == id_number).first()

def create(db: Session, channel_user: ChannelUserSchema, channel_type: str):

    db_channel_user = select_by_user_id(db, channel_user.user_id, channel_type)
    db_customer = select_customer_by_id_number(db, channel_user.id_number)

    if not db_customer:
        raise HTTPException(status_code=400, detail="ID Number doesnt exist") 
    
    if db_channel_user:
        raise HTTPException(status_code=400, detail="User ID exists") 

    db_channel_user = ChannelUserModel(
        user_id = channel_user.user_id,
        password = channel_user.password,
        name = channel_user.name,
        channel_type = channel_type,
        customer_id = db_customer.id
    )

    db.add(db_channel_user)
    db.commit()
    db.refresh(db_channel_user)

    return db_channel_user

def all(db:Session, channel_type: str, skip: int = 0, limit: int = 100):
    return { "data" : db.query(ChannelUserModel).filter(ChannelUserModel.channel_type == channel_type).offset(skip).limit(limit).all() }

def detail(db: Session, user_id: str, channel_type: str):
    db_channel_user = select_by_user_id(db, user_id, channel_type)
    if db_channel_user: 
        return { 'data' : db_channel_user, 'customer_info' : db_channel_user.customers, 'account_info' : db_channel_user.customers.accounts }
    else:
        raise HTTPException(status_code=400, detail="User ID doesnt exist") 

def update(db: Session, channel_user: ChannelUserUpdateSchema, user_id: str, channel_type: str):
    db_channel_user = select_by_user_id(db, user_id, channel_type)

    if not db_channel_user: 
        raise HTTPException(status_code=400, detail="User ID doesnt exist") 
    
    setattr(db_channel_user, "name", channel_user.name)

    db.commit()
    db.refresh(db_channel_user)
    
    return db_channel_user

def update_password(db: Session, channel_user: ChannelUserUpdatePasswordSchema, user_id: str, channel_type: str):
    db_channel_user = select_by_user_id(db, user_id, channel_type)

    if not db_channel_user: 
        raise HTTPException(status_code=400, detail="User ID doesnt exist") 
    
    if db_channel_user.password != channel_user.old_password:
        raise HTTPException(status_code=400, detail="Invalid Password") 

    setattr(db_channel_user, "password", channel_user.password)

    db.commit()

    return { "message" : "password updated!" }

def login(db: Session, channel_user: ChannelUserLoginSchema, channel_type: str):
    db_channel_user = select_by_user_id(db, channel_user.user_id, channel_type)

    if not db_channel_user: 
        raise HTTPException(status_code=400, detail="User ID doesnt exist") 
    
    if db_channel_user.password != channel_user.password:
        raise HTTPException(status_code=400, detail="Invalid Password") 

    return db_channel_user

def delete(db: Session, user_id: str, channel_type: str):
    db_channel_user = select_by_user_id(db, user_id, channel_type)
    if db_channel_user:
        db.delete(db_channel_user)
        db.commit()
    return { "message" : f"{user_id} has bee deleted!" }

