import datetime
from pydantic import BaseModel
from typing import Optional

#Account schema
class RoleBase(BaseModel):
    role : str
    is_active : bool = True
    

#Account create schema
class RoleCreate(RoleBase):
    pass


#Account update schema
class RoleUpdate(RoleBase):
    pass
    
   
        
        

class Role(RoleBase):
    id : Optional[int]
    role : Optional[str]
    is_active : Optional[bool]
    created_at : datetime.datetime = datetime.datetime.now()
    updated_at : datetime.datetime = datetime.datetime.now()
    
    
    class config:
        orm_mode = True