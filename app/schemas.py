from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserRegister(UserBase):
    username : str
    
class UserLogin(UserBase):
    pass

class Post(BaseModel):
    note: str

class ResetRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str