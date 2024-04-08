from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import session
from config import get_db
from utils.constants import Messages
from . import schemas, services

#create API instance

role_router = APIRouter(
    
    prefix= '/role',
    tags = ['role'],
    responses={404 : {"Description" : "Not found"}},
    
)

@role_router.get("/", response_model=List[schemas.Role])
async def get_all_role(skip: int =0, limit: int = 100,db: session = Depends(get_db)):
    roles =  services.get_all_role(db=db, skip=skip, limit=limit)
    return roles


#get by id
@role_router.get("/{role_id}", response_model= schemas.Role, status_code= status.HTTP_200_OK)
async def get_role(role_id = int, db: session = Depends(get_db)):
    role = services.get_by_role_id(db=db, account_id= role_id)
    if not role:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= Messages.ROLE_NOT_FOUND)
    return role


#create new account
@role_router.post("/", response_model= schemas.Role, status_code= status.HTTP_201_CREATED)
async def create_role(role : schemas.RoleCreate, db: session =Depends(get_db)):
    existing_role = services.get_by_role_name(db=db, role_name=role.role )
    if existing_role:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= Messages.ROLE_ALREADY_EXIST)
    new_role = services.create_role(db=db, role=role)
    return new_role

#update account
@role_router.put('/{role_id}', response_model= schemas.Role, status_code=status.HTTP_200_OK)
async def update_role(role_id : int, role: schemas.RoleUpdate, db: session=Depends(get_db)):
    existing_role = services.get_by_role_id(db=db, role_id = role_id)
    
    if not  existing_role:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= Messages.ROLE_NOT_FOUND)
     
    updated_role = services.update_role(db=db, role_id=role_id, role=role)
    return updated_role

@role_router.delete('/{role_id}', status_code= status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: int, db: session = Depends(get_db)):
    existing_role = services.get_by_role_id(db=db, role_id=role_id)
    if not existing_role:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= Messages.ROLE_NOT_FOUND)
    services.delete_role(db=db, role_id=role_id)
    return{"Messages" : Messages.ACCOUNT_DELETED}
        