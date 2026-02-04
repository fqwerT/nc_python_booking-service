from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from fastapi import HTTPException, status
from jose import JWTError, jwt

from auth.repository.auth_repository import AuthRepository
from auth.schemas.auth_schemas import Token, UserCreate, UserLogin, UserRead, UserAuthResponse
from config import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET_KEY
import uuid

JWT_EXPIRE_MINUTES = 15                  
JWT_REFRESH_EXPIRE_DAYS = 7                


    
class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def _hash_password(self, password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)



    def _create_access_token(self, subject: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
        to_encode = {"sub": subject, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    def decode_token(self, token: str) -> str:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось проверить учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            subject: Optional[str] = payload.get("sub")
            if subject is None:
                raise credentials_exception
            return subject
        except JWTError:
            raise credentials_exception

    def register_user(self, user_in: UserCreate) -> UserAuthResponse:
        existing = self.auth_repository.get_user_by_email(user_in.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким e-mail уже существует",
            )

        password_hash = self._hash_password(user_in.password)
        unique_id = str(uuid.uuid4())
        user = self.auth_repository.create_user(
            email=user_in.email,
            full_name=user_in.full_name,
            avatar=user_in.avatar or "",
            password_hash=password_hash,
            id=unique_id
         
        )
        access_token = self._create_access_token(subject=user_in.email)
        refresh_token = self._create_refresh_token(subject=user_in.email)
        return UserAuthResponse(
            user=UserRead.model_validate(user),
            access_token=access_token,
            refresh_token=refresh_token
        )

    def login(self, credentials: UserLogin) -> UserAuthResponse:
        user = self.auth_repository.get_user_by_email(credentials.email)
 
        if not user or not self._verify_password(
            credentials.password, user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный e-mail или пароль",
            )

        access_token = self._create_access_token(subject=user.email)
        refresh_token = self._create_refresh_token(subject=user.email)
        return  UserAuthResponse(
            user=UserRead.model_validate(user),
            access_token=access_token,
            refresh_token=refresh_token
        )
    def _create_refresh_token(self, subject: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=JWT_REFRESH_EXPIRE_DAYS)
        to_encode = {
            "sub": subject,
            "exp": expire,
            "type": "refresh"          # для отличия от access token
        }
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    def decode_refresh_token(self, token: str) -> str:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            if payload.get("type") != "refresh":
                raise credentials_exception
            subject: Optional[str] = payload.get("sub")
            if subject is None:
                raise credentials_exception
            return subject
        except JWTError:
            raise credentials_exception


    def refresh_token(self, refresh_token: str) -> UserAuthResponse:
        # Декодируем refresh token
        subject = self.decode_refresh_token(refresh_token)

        # Получаем пользователя
        user = self.auth_repository.get_user_by_email(subject)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден"
            )

        # Создаём новые токены (token rotation — рекомендуется даже в простом варианте)
        new_access_token = self._create_access_token(subject=subject)
        new_refresh_token = self._create_refresh_token(subject=subject)

        return UserAuthResponse(
            user=UserRead.model_validate(user),
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )

