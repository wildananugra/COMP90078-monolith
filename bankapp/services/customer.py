from schemas.customer import *
from sqlalchemy.orm import Session
from models.customer import CustomerModel
from fastapi import HTTPException

import random
import string

# utils
def generate_cif_number(size=10):
    return ''.join(random.choice(string.digits) for _ in range(size))

def select_by_cif(db: Session, cif_number):
    return db.query(CustomerModel).filter(CustomerModel.cif_number == cif_number).first()

def select_by_id_number(db: Session, id_number):
    return db.query(CustomerModel).filter(CustomerModel.id_number == id_number).first()

# services
def create(db: Session, user: CustomerSchema):
    
    user_dict = user.dict()    
    
    user_dict['cif_number'] = generate_cif_number()
    while select_by_cif(db, user_dict['cif_number']):
        user_dict['cif_number'] = cif_number()

    if select_by_id_number(db, user.id_number):
        raise HTTPException(status_code=400, detail="ID Number already registered") 

    db_user = CustomerModel(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user_dict

def all(db: Session, skip: int = 0, limit: int = 100):
    customers = db.query(CustomerModel).offset(skip).limit(limit).all()
    responses = []
    for customer in customers:
        responses.append({
            "name":customer.name,
            "id_number" : customer.id_number,
            "cif_number" : customer.cif_number,
            "email" : customer.email
        })
    return { "data" : responses }

def delete(db: Session, cif_number: str):
    customer = select_by_cif(db, cif_number=cif_number)
    if customer:
        db.delete(customer)
        db.commit()
    return customer
    
def detail(db: Session, id_number: str):
    customer = select_by_id_number(db, id_number)
    
    if customer:
        return CustomerCreateSchema(
            name = customer.name,
            id_number = customer.id_number,
            email= customer.email,
            cif_number = customer.cif_number
        ).dict()
    else:
        raise HTTPException(status_code=404, detail="ID Number not registered") 
    
def update(db: Session, customer: CustomerSchema, cif_number: str):
    customer_existing = select_by_cif(db, cif_number=cif_number)
    
    customer_dict = customer.dict(exclude_unset=True)
    if customer_existing:
        for key, value in customer_dict.items():
            setattr(customer_existing, key, value)
        db.commit()
    return customer