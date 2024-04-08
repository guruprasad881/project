import datetime
from pydantic import BaseModel
from typing import Optional

#Account schema
class AccountBase(BaseModel):
    name : str
    is_active : bool = True
    

#Account create schema
class AccountCreate(AccountBase):
    pass


#Account update schema
class AccountUpdate(AccountBase):
    name: Optional[str] = None
    is_active : Optional[bool] = None
    
    class config:
        orm_mode = True
    
   
        
        

class Account(AccountBase):
    id : Optional[int]
    name : Optional[str]
    is_active : Optional[bool]
    created_at : datetime.datetime = datetime.datetime.now()
    updated_at : datetime.datetime = datetime.datetime.now()
    
    
    class config:
        orm_mode = True