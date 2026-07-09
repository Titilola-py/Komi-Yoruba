from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.schemas import UserLoginRequest, UserRegisterRequest, UserRegisterResponse, TokenResponse
from app.auth.service import AuthService
from app.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegisterRequest, db: Session = Depends(get_db)) -> UserRegisterResponse:
    service = AuthService(db)
    return service.register_user(payload)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(payload: UserLoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """Authenticate user and return JWT access token.

    Args:
        payload: User login credentials (email and password).
        db: Database session.

    Returns:
        TokenResponse containing JWT access token.

    Raises:
        HTTPException 401: If credentials are invalid.
        HTTPException 403: If user account is inactive.
        HTTPException 500: If database error occurs.
    """
    service = AuthService(db)
    return service.authenticate_user(payload)
