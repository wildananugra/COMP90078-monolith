from schemas.customer_service import *
from sqlalchemy.orm import Session
from models.customer_service import CustomerServiceModel
from fastapi import HTTPException

# utils
def select_by_user_id(db: Session, user_id: str):
    return db.query(CustomerServiceModel).filter(CustomerServiceModel.user_id == user_id).first()

def create(db: Session, customer_service: CustomerServiceSchema):

    db_customer_service = select_by_user_id(db, customer_service.user_id)

    if db_customer_service:
        raise HTTPException(status_code=400, detail="User ID exists") 

    db_customer_service = CustomerServiceModel(
        user_id = customer_service.user_id,
        password = customer_service.password,
        name = customer_service.name
    )

    db.add(db_customer_service)
    db.commit()
    db.refresh(db_customer_service)

    return db_customer_service

def all(db:Session, skip: int = 0, limit: int = 100):
    return { "data" : db.query(CustomerServiceModel).offset(skip).limit(limit).all() }

def detail(db: Session, user_id: str):
    db_customer_service = select_by_user_id(db, user_id)
    if db_customer_service: 
        return db_customer_service
    else:
        raise HTTPException(status_code=400, detail="User ID doesnt exist") 

def update(db: Session, customer_service: CustomerServiceUpdateSchema, user_id: str):
    db_customer_service = select_by_user_id(db, user_id)

    if not db_customer_service: 
        raise HTTPException(status_code=400, detail="User ID doesnt exist") 
    
    setattr(db_customer_service, "name", customer_service.name)

    db.commit()
    db.refresh(db_customer_service)
    
    return db_customer_service

def update_password(db: Session, customer_service: CustomerServiceUpdatePasswordSchema, user_id: str):
    db_customer_service = select_by_user_id(db, user_id)

    if not db_customer_service: 
        raise HTTPException(status_code=400, detail="User ID doesnt exist") 
    
    if db_customer_service.password != customer_service.old_password:
        raise HTTPException(status_code=400, detail="Invalid Password") 

    setattr(db_customer_service, "password", customer_service.password)

    db.commit()

    return { "message" : "password updated!" }

def login(db: Session, customer_service: CustomerServiceLoginSchema):
    db_customer_service = select_by_user_id(db, customer_service.user_id)

    if not db_customer_service: 
        raise HTTPException(status_code=400, detail="User ID doesnt exist") 
    
    if db_customer_service.password != customer_service.password:
        raise HTTPException(status_code=400, detail="Invalid Password") 

    return db_customer_service

def delete(db: Session, user_id: str):
    db_customer_service = select_by_user_id(db, user_id)
    if db_customer_service:
        db.delete(db_customer_service)
        db.commit()
    return { "message" : f"{user_id} has bee deleted!" }

