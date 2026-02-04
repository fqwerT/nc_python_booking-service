from fastapi import APIRouter, Depends

from auth.dependencies import get_auth_service, get_current_user
from auth.schemas.auth_schemas import Token, UserCreate, UserLogin, UserRead, UserAuthResponse, RefreshTokenRequest
from auth.service.auth_service import AuthService
from auth.model.auth_model import User

router = APIRouter()


@router.post("/register", response_model=UserAuthResponse, summary="Регистрация нового пользователя")
def register_user(user_in: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.register_user(user_in)


@router.post("/login", response_model=UserAuthResponse, summary="Аутентификация пользователя")
def login(credentials: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.login(credentials)

@router.post(
    "/refresh",
    response_model=UserAuthResponse,
    summary="Обновление access-токена с помощью refresh-токена"
)
def refresh_token(
    token_data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.refresh_token(token_data.refresh_token)


@router.get("/me", response_model=UserRead, summary="Информация о текущем пользователе")
def read_current_user(current_user: User = Depends(get_current_user)):
    return UserRead.model_validate(current_user)


