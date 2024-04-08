from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import session
from config import get_db
from utils.constants import Messages
from . import schemas, services

#create API instance

account_router = APIRouter(
    
    prefix= '/account',
    tags = ['account'],
    responses={404 : {"Description" : "Not found"}},
    
)

@account_router.get("/", response_model=List[schemas.Account])
async def get_all_account(skip: int =0, limit: int = 100,db: session = Depends(get_db)):
    accounts =  services.get_all_accounts(db=db, skip=skip, limit=limit)
    return accounts


#get by id
@account_router.get("/{account_id}", response_model= schemas.Account, status_code= status.HTTP_200_OK)
async def get_account(account_id = int, db: session = Depends(get_db)):
    account = services.get_by_account_id(db=db, account_id= account_id)
    if not account:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= Messages.ACCOUNT_NOT_FOUND)
    return account


#create new account
@account_router.post("/", response_model= schemas.Account, status_code= status.HTTP_201_CREATED)
async def create_account(account : schemas.AccountCreate, db: session =Depends(get_db)):
    existing_account = services.get_by_account_name(db=db, account_name=account.name )
    if existing_account:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= Messages.ACCOUNT_ALREADY_EXIST)
    new_account = services.create_account(db=db, account=account)
    return new_account

#update account
@account_router.put('/{account_id}', response_model= schemas.Account, status_code=status.HTTP_200_OK)
async def update_account(account_id : int, account: schemas.AccountUpdate, db: session=Depends(get_db)):
    existing_account = services.get_by_account_id(db=db, account_id = account_id)
    
    if not  existing_account:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= Messages.ACCOUNT_NOT_FOUND)
     
    updated_account = services.update_account(db=db, account_id=account_id, account=account)
    return updated_account

@account_router.delete('/{account_id}', status_code= status.HTTP_204_NO_CONTENT)
async def delete_account(account_id: int, db: session = Depends(get_db)):
    existing_account = services.get_by_account_id(db=db, account_id=account_id)
    if not existing_account:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= Messages.ACCOUNT_NOT_FOUND)
    services.delete_account(db=db, account_id=account_id)
    return{"Messages" : Messages.ACCOUNT_DELETED}
        