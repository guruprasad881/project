from . import models, schemas
from sqlalchemy.orm import Session
from account.models import Account_model
#get all accounts
def get_all_accounts(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Account_model).offset(skip).limit(limit).all()

#get by id
def get_by_account_id(db: Session, account_id : int):
    #select * from account WHERE id='1'
    return db.query(models.Account_model).filter(models.Account_model.id == account_id).first()

#get by name
def get_by_account_name(db: Session, account_name: str):
    #select * from account WHERE name='1'
    return db.query(models.Account_model).filter(models.Account_model.name == account_name).first()

#create account
def create_account(db: Session, account : schemas.AccountCreate):
    new_accounts = models.Account_model(**account.dict())
    db.add(new_accounts)
    db.commit()
    db.refresh(new_accounts)
    return new_accounts

#update account
def update_account(db: Session, account_id: int, account: schemas.AccountUpdate):
    #retrieve account
    existing_account = db.query(Account_model).filter(Account_model.id == account_id)
    if not existing_account.first():
          return ValueError(f"Account id {account_id} not found")
    existing_account.update(account.dict())
    db.commit()
    return existing_account

#delete account
def delete_account(db: Session, account_id : int):
    existing_account = db.query(models.Account_model).filter(models.Account_model.id == account_id)
    if not existing_account.first():
        raise ValueError(f"Account id {account_id} not found")
    existing_account.delete()
    db.commit()
    


