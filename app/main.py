from fastapi import FastAPI
from app.database import Base, engine
from app import model
from app.routers import auth,password_reset, refresh_token, notes
from app.config import settings

REFRESH_TOKEN_SECRET_KEY = settings.REFRESH_TOKEN_SECRET_KEY
#this basically creates all the tables that are imported in this file 
model.Base.metadata.create_all(bind=engine) 

app = FastAPI()

app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(password_reset.router)
app.include_router(refresh_token.router)

@app.get("/")
def root():
    return {"message": "MindVault API is working"}

