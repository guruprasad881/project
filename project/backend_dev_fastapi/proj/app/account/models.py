from datetime import datetime
from sqlalchemy import String, Integer, Column, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship


from config import base

class Account_model(base):
    __tablename__ = "Account"

    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    #account_id = Column(Integer, nullable = False, unique = True)
    name = Column(String(length=50), nullable = False)
    is_active = Column(TINYINT(1), nullable = False, default = 1)
    created_at = Column(DateTime, nullable = False, default = datetime.now())
    updated_at = Column(DateTime, nullable = False, default = datetime.now(), onupdate = datetime.now())
    
    Users = relationship('UserModel', back_populates = 'Account')
    
    def __repr__(self):
        return f"Account name : {self.name}"

