from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException
from schemas.parameter import *
from models.parameter import ParameterModel
import string, random

def select_by_type_key(db: Session, type: str, key: str):
    return db.query(ParameterModel).filter(and_(ParameterModel.parameter_type == type, ParameterModel.key == key)).first()

def create(db: Session, parameter: ParameterSchema):

    if select_by_type_key(db, parameter.parameter_type, parameter.key):
        raise HTTPException(status_code=400, detail="Type and key exists")

    db_parameter = ParameterModel(
        parameter_type = parameter.parameter_type,
        key = parameter.key,
        value = parameter.value,
        description = parameter.description
    )

    db.add(db_parameter)
    db.commit()
    db.refresh(db_parameter)

    return db_parameter

def by_type(db: Session, parameter_type: str):
    db_parameter = db.query(ParameterModel).filter(ParameterModel.parameter_type == parameter_type).all()
    if db_parameter:
        return db_parameter
    else:
        raise HTTPException(status_code=404, detail="Type not found")

def by_key(db: Session, parameter_type: str, key: str):
    db_parameter = select_by_type_key(db, parameter_type, key)
    if db_parameter:
        return db_parameter
    else:
        raise HTTPException(status_code=404, detail="Type and key not found")

def all(db: Session, skip: int = 0, limit: int = 0):
    db_parameter = db.query(ParameterModel).offset(skip).limit(limit).all()
    db.close()
    return db_parameter

def delete(db: Session, parameter_type: str, key: str):
    db_parameter = select_by_type_key(db, parameter_type, key)
    if db_parameter:
        db.delete(db_parameter)
        db.commit()
        return { "message" : f"{parameter_type} -> {key} has been deleted" }
    else: 
        raise HTTPException(status_code=404, detail="Type and key not found")
    