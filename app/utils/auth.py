from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.utils.jwt import verify_jwt
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # this is the route name

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_jwt(token, settings.ACCESS_TOKEN_SECRET_KEY)
        return payload
        # email: str = payload.get("sub")
        # if email is None:
        #     raise credentials_exception
        # return email  # or load user from DB here
    except JWTError:
        raise credentials_exception