from datetime import datetime
from sqlalchemy import Column,Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from role.models import Role_model
from config import base

class UserModel(base):
    
    __tablename__ = "Users"
    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    email = Column(String(255),nullable= False, unique= True, index = True)
    password = Column(String(1024), nullable= False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    role_id = Column(Integer, ForeignKey('Role.id'), nullable= False)
    account_id = Column(Integer, ForeignKey('Account.id'), nullable= False) 
    is_active = Column(TINYINT, default= True)
    created_at = Column(DateTime, default= datetime.now())
    updated_at = Column(DateTime, default= datetime.now(), onupdate= datetime.now())
    
    Role = relationship('Role_model', back_populates = 'Users')
    Account = relationship('Account_model', back_populates = 'Users')
    
    
    def __repr__(self):
        return f"UserModel(id = {self.id}, email={self.email})"