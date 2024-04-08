import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from config import setting
from passlib.context import CryptContext





pwd_context = CryptContext(schemes= ['bcrypt'], deprecated = "auto")






def hash_password(password):
   return pwd_context.hash(password)

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: int, expires_delta : timedelta= None):
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes= setting.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        
    to_encode = {"exp": expire, "sub": str(data)}
    
#encoded text
    encoded_jwt = jwt.encode(to_encode, setting.JWT_SECRET_KEY, algorithm = setting.ALGORITHM )
    return encoded_jwt


def create_refresh_token(data: int, expires_delta : timedelta = None):
    
    if expires_delta:
        expire= datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes= setting.REFRESH_TOKEN_EXPIRE_MINUTES)
        
    to_encode = {"exp": expire, "sub": str(data)}
    
    #encoded text
    encoded_jwt = jwt.encode(to_encode, setting.JWT_REFRESH_SECRET_KEY, algorithm= setting.ALGORITHM)
    return encoded_jwt
    
    
    