from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    avatar: str | None = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str  
    exp: datetime


class UserAuthResponse(BaseModel):
    user: UserRead
    access_token: str
    refresh_token:str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token:str
