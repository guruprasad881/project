
from fastapi import Depends, HTTPException, status
from jose import jwt
from datetime import datetime
from config import setting, get_db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from pydantic import ValidationError
from utils.constants import Messages
from users.schemas import TokenPayload
from users.service import get_user_by_id
from passlib.context import CryptContext





#password context
pwd_context = CryptContext(schemes= ['bcrypt'], deprecated = "auto")



#OAuth2scheme
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl= "/user/login", scheme_name = "JWT")

#get current user
async def get_current_user(token: str = Depends(reusable_oauth2), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token,
                             setting.JWT_SECRET_KEY,
                             algorithms= [setting.ALGORITHM])
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(int(token_data.exp)) < datetime.utcnow():
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                                detail= Messages.TOKEN_EXPIRED,
                                headers={"WWW--Authenticate" : "Bearer"})
        
        
    except(JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail= Messages.INVALID_TOKEN,
                            headers= {"WWW-Authenticate" : "Bearer"})
    
    user = get_user_by_id(db, token_data.sub)
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= Messages.USER_NOT_FOUND)
    return user