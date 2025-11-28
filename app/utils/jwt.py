from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.config import settings

ACCESS_TOKEN_SECRET_KEY = settings.ACCESS_TOKEN_SECRET_KEY
REFRESH_TOKEN_SECRET_KEY = settings.REFRESH_TOKEN_SECRET_KEY
RESET_TOKEN_SECRET_KEY = settings.RESET_TOKEN_SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
ALGORITHM = settings.JWT_ALGORITHM


def create_access_token(data: dict):
    to_encode = data.copy() 
    expiry = datetime.now()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": int(expiry.timestamp()) })
    print("Access token expires at:", expiry)

    return jwt.encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(id: str):
    expiry = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"id":id,"exp": int(expiry.timestamp()) }
    return jwt.encode(to_encode,REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)

def create_email_reset_token(data: dict):
    to_encode = data.copy()
    expiray = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp":expiray})
    return jwt.encode(to_encode, RESET_TOKEN_SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt(token: str, secret_key:str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        print("JWT verification error:", e)
        return None
