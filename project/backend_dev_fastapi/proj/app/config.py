import os                                                       #to read filesystem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base    #to create the session
from pydantic import BaseSettings

from dotenv import load_dotenv

#load environment variables
load_dotenv()

#read environment variables
ENVIRONMENT = os.getenv("ENV")


#Database configuration
if ENVIRONMENT:
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DB_URI")
else:
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DB_URI")
    
    
print(SQLALCHEMY_DATABASE_URI)


#create engine
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

#create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#create base
base = declarative_base()

#Dependency
def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()
        
        
        

class Settings(BaseSettings):
    
    ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
    ALGORITHM = "HS256"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")
    
setting = Settings()
    