from datetime import datetime
from sqlalchemy import String, Integer, Column, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship


from config import base

class Role_model(base):
    __tablename__ = "Role"

    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    #account_id = Column(Integer, nullable = False, unique = True)
    role = Column(String(length=20), nullable = False)
    is_active = Column(TINYINT(1), nullable = False, default = 1)
    created_at = Column(DateTime, nullable = False, default = datetime.now())
    updated_at = Column(DateTime, nullable = False, default = datetime.now(), onupdate = datetime.now())
    
    Users = relationship('UserModel', back_populates = 'Role')
    
    def __repr__(self):
        return f"Role name : {self.role}"



