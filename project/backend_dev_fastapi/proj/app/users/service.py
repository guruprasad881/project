from sqlalchemy.orm import Session
from sqlalchemy import update
from fastapi import HTTPException, status

from role.models import Role_model
from account.models import Account_model

from utils.security import hash_password, verify_password

from .models import UserModel
from .schemas import UserCreate, UserUpdate

#get all users
def get_all_users(db: Session, skip: int=0, limit: int =100):
    return db.query(UserModel).offset(skip).limit(limit).all()

#get user by id
def get_user_by_id(db:Session, user_id: int):
    return db.query(UserModel).get(user_id)
    
    
#get user by email
def get_user_by_email(db:Session, email: str):
    return db.query(UserModel).filter(UserModel.email.contains(email)).first()
    
    
#create user
def create_user(db:Session, users: UserCreate):
    role = db.query(UserModel).filter(Role_model.id == users.role_id).first()
    if not role:
        ValueError("Role not found")
    
    account = db.query(UserModel).filter(Account_model.id == users.account_id).first()
    if not account:
        ValueError("Account not found")
        
    hashed_password = hash_password(users.password)
    
    user_data = users.dict()       
    user_data['password'] = hashed_password 
    
    new_user = UserModel(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#update existing user
def update_user(db: Session, user_id : int, users: UserUpdate):
    existing_user = db.query(UserModel).filter(UserModel.id == user_id)
    if not existing_user.first():
        raise ValueError(status_code= status.HTTP_404_NOT_FOUND, detail = "user not found")
    
    existing_user.update(users.dict())
    db.commit()
    return existing_user.first()


#delete user
def delete_user(db:Session, user_id: int):
    existing_user = db.query(UserModel).filter(UserModel.id == user_id)
    if not existing_user.first():
        raise ValueError(status_code= status.HTTP_404_NOT_FOUND,detail = "User not found")
    
    existing_user.delete(synchronize_session = False)
    db.commit()
    return existing_user.first()


#authenticate user
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    
    return user