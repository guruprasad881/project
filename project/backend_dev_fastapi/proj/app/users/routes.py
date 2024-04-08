
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from utils.constants import Messages
from utils.security import create_access_token, create_refresh_token
from config import get_db, setting
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from utils.deps import get_current_user




from . import schemas, service

user_router = APIRouter(
    
    prefix= "/user",
    tags = ['user']   
)



@user_router.get('/me', response_model= schemas.User)
def get_current_user(user: schemas.User = Depends(get_current_user)):
    return user


#get all users
@user_router.get("/", response_model= List[schemas.User])
def get_all_user(skip: int=0, limit: int = 100, db: Session= Depends(get_db)):
    return service.get_all_users(db, skip, limit)


#get user by id
@user_router.get('/{user_id}', response_model= schemas.User)
def get_user_by_id(user_id : int, db: Session= Depends(get_db)):
    users = service.get_user_by_id(db, user_id)
    
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= Messages.USER_NOT_FOUND)
    
    return users

#create user
@user_router.post('/', response_model= schemas.User, status_code= status.HTTP_404_NOT_FOUND )
def create_user(users: schemas.UserCreate, db: Session = Depends(get_db)):
    #check user already exist
    existing_user = service.get_user_by_email(db, users.email)
    if existing_user:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= Messages.USER_ALREADY_EXIST)
    
    
    try:
        created_user= service.create_user(db, users)
       
    except ValueError as e:
       if str(e) == "Role not found":
           raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail=Messages.ROLE_NOT_FOUND)
       elif str(e) == "Account not found":
           raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= Messages.ACCOUNT_NOT_FOUND)
       else:
           raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(e))
       
    
    return created_user


@user_router.put("/{user_id}", response_model= schemas.User)
def update_user(user_id: int, users: schemas.UserUpdate, db: Session = Depends(get_db)):
    existing_user = service.get_user_by_id(db, user_id)
    
    if not existing_user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= Messages.USER_NOT_FOUND)
    
    return service.update_user(db, user_id, users)


@user_router.delete("/{user_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_user(user_id : int, db: Session = Depends(get_db)):
    existing_user = service.get_user_by_id(db, user_id)
    
    if not existing_user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = Messages.USER_NOT_FOUND)
    
    service.delete_user(db, user_id)
    
    res = {
        
        "status" : True,
        "Message" : Messages.USER_DELETED
        
    }
       
    return res


#login
@user_router.post('/login', response_model= schemas.Token )
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = service.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= Messages.USER_UNAUTHORIZED)
    
    res = {
        
        "access_token" : create_access_token(user.id),
        "token_type" : "bearer",
        "expires_in" : timedelta(minutes= setting.ACCESS_TOKEN_EXPIRE_MINUTES),
        "refresh_token" : create_refresh_token(user.id)
        
        }
    
    return res



@user_router.post('/logout', status_code= status.HTTP_204_NO_CONTENT)
def logout(current_user: schemas.User = Depends()):
    return {'message' : 'logout successfully'}