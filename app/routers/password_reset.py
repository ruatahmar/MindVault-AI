from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from jose import JWTError
from app import schemas, model
from app.utils.jwt import create_email_reset_token, verify_jwt
from app.utils.email import send_reset_email
from app.utils.password_hash import hash_pwd, verify_pwd
from app.database import get_db
from app.config import settings

router = APIRouter(
    prefix="",
    tags=["Password Reset"]
)

SECRET_KEY=settings.RESET_TOKEN_SECRET_KEY

@router.post("/forget-password")
async def password_reset(payload: schemas.ResetRequest, db: Session = Depends(get_db)):
    email = payload.email
    user = db.query(model.User).filter(model.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email is not registered")
    
    token = create_email_reset_token({"sub": user.email})
    await send_reset_email(user.email, token)
    return {"msg": "Password reset link sent"}



@router.post("/reset-password")
async def reset_password(req: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    token = req.token
    new_password = req.new_password
    try:
        payload = verify_jwt(token, SECRET_KEY)
        email: str = payload.get("sub")
        if email is None:
            raise JWTError()
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(model.User).filter(model.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_pwd(new_password)
    db.commit()
    return {"msg": "Password reset successful"}


@router.get("/reset-password")
def validate_token(token: str):
    try:
        payload = verify_jwt(token, SECRET_KEY)
        return {"msg": "Valid token", "email": payload["sub"]}
    except:
        raise HTTPException(400, "Invalid or expired token")