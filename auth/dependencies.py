from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth.model.auth_model import User
from auth.repository.auth_repository import AuthRepository
from auth.service.auth_service import AuthService
from db_init import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_auth_repository(db: Session = Depends(get_db)) -> AuthRepository:
    return AuthRepository(db)


def get_auth_service(repo: AuthRepository = Depends(get_auth_repository)) -> AuthService:
    return AuthService(repo)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
    db: Session = Depends(get_db),
) -> User:
    email = auth_service.decode_token(token)
    repo = AuthRepository(db)
    user = repo.get_user_by_email(email)
    if not user:
        # Если пользователь не найден, токен считаем недействительным
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден или токен недействителен",
        )
    return user


