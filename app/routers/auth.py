from app import schemas, model
from app.utils.password_hash import hash_pwd, verify_pwd
from app.utils.jwt import create_access_token, create_refresh_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends
from app.database import get_db

router = APIRouter(
    prefix="",
    tags=["Authentication"]

)

@router.post("/register")
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    hashed_pw = hash_pwd(user.password)
    created_user = model.User(username=user.username, email=user.email, password=hashed_pw)
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    access_token=create_access_token({"id":created_user.id})
    refresh_token=create_refresh_token(str(created_user.id))
    response = JSONResponse({"access token": access_token})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict"
    )
    return response

@router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = user.username
    user_exists = db.query(model.User).filter(model.User.email == email).first()
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not registered")

    if not verify_pwd(user.password, user_exists.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password")    
    access_token = create_access_token({"id":user_exists.id})
    refresh_token = create_refresh_token(str(user_exists.id))
    response = JSONResponse({"access_token" : access_token})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # only over HTTPS
        samesite="strict"
    )
    return response

