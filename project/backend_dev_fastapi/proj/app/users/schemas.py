import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

from role.schemas import Role
from account.schemas import Account




class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role_id : int
    account_id : int
    is_active: bool = True
    
class UserCreate(UserBase):
   password: str
    
    
class UserUpdate(UserBase):
    # email : Optional[EmailStr] = None
    # first_name : Optional[str]= None
    # last_name : Optional[str] = None
    # role_id : Optional[int] = None
    # account_id : Optional[int] = None
    # is_active: Optional[bool] = None
    pass
   
        
    
    
        

        
class User(UserBase):
    id : int
    email: EmailStr
    first_name: str
    last_name: str
    password : str
    role_id : int
    account_id : int
    is_active: int
    created_at : datetime.datetime = datetime.datetime.now()
    updated_at : datetime.datetime = datetime.datetime.now()
    
    class config:
        orm_mode = True
        
#token schema
class Token(BaseModel):
    access_token: str
    token_type : str
    expires_in : datetime.timedelta
    refresh_token : str
    
    
class TokenData(BaseModel):
    email: Optional[str] = None
    
    
class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[str] = None