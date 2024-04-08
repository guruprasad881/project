
 
#import uvicorn
from fastapi import FastAPI
from config import SessionLocal

from account.routes import account_router
from role.routes import role_router
from users.routes import user_router
 

app =  FastAPI(title="Restroom management")

app.include_router(account_router)
app.include_router(role_router)
app.include_router(user_router)



@app.get("/")
async def root():
    return {"message" : " world"}

#if __name__ == "__main__":
    #uvicorn.run(app, host="0.0.0.0", port=8080)