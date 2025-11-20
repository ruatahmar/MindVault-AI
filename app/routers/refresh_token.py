from app.config import settings
from fastapi import Request, status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.jwt import verify_jwt,create_access_token
from app.model import User
from app.database import get_db
router = APIRouter(
    prefix="",
    tags=["Refresh Token"]
)

REFRESH_TOKEN_SECRET_KEY=settings.REFRESH_TOKEN_SECRET_KEY

@router.post("/refresh")
def refresh_token(request: Request, db: Session = Depends(get_db) ):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Refresh token not found")
    try:
        payload = verify_jwt(refresh_token, REFRESH_TOKEN_SECRET_KEY)
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid refresh token")
    except:
        raise HTTPException(status_code=401,detail="Invalid or expired tokens.")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User no longer exists")
    
    new_access_token = create_access_token({"sub": str(user.id)})
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

