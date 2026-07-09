from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.auth.jwt import create_access_token
from app.auth.password import hash_password, verify_password
from app.auth.repository import UserRepository
from app.auth.schemas import UserLoginRequest, UserRegisterRequest, UserRegisterResponse, TokenResponse
from app.models import User


class AuthService:
    """Business logic layer for user authentication operations.

    Handles validation, duplicate checking, and transaction management.
    """

    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = UserRepository(db)

    def register_user(self, payload: UserRegisterRequest) -> UserRegisterResponse:
        """Register a new user with email, username, and password.

        Validates that email and username are unique, then creates the user
        in the database with a hashed password.

        Args:
            payload: User registration request with email, username, display_name, password.

        Returns:
            UserRegisterResponse with created user details (no password).

        Raises:
            HTTPException: If email or username already registered, or database error occurs.
        """
        # Check for duplicate email
        if self.repository.get_by_email(payload.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email already registered")

        # Check for duplicate username
        if self.repository.get_by_username(payload.username):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already taken")

        # Create new user with hashed password
        user = User(
            email=payload.email,
            username=payload.username,
            display_name=payload.display_name,
            hashed_password=hash_password(payload.password),
        )

        try:
            # Create user (repository uses flush, not commit)
            created_user = self.repository.create(user)
            # Commit transaction after successful creation
            self.db.commit()
        except SQLAlchemyError as e:
            # Rollback on any database error
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to register user",
            ) from e

        # Use model_validate to create response directly from ORM object
        return UserRegisterResponse.model_validate(created_user)

    def authenticate_user(self, payload: UserLoginRequest) -> TokenResponse:
        """Authenticate a user and return a JWT access token.

        Validates user credentials (email and password), checks user status,
        and generates a JWT token for authenticated access.

        Args:
            payload: User login request with email and password.

        Returns:
            TokenResponse containing JWT access token and token type.

        Raises:
            HTTPException 401: If user not found or password is incorrect.
            HTTPException 403: If user account is not active.
            HTTPException 500: If database error occurs.
        """
        try:
            # Look up user by email
            user = self.repository.get_by_email(payload.email)

            # If user not found or password incorrect, return 401
            if not user or not verify_password(payload.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # If user is inactive, return 403
            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User account is inactive",
                )

            # Generate JWT access token
            access_token = create_access_token(user_id=user.id, email=user.email)

            # Return token response
            return TokenResponse(access_token=access_token, token_type="bearer")

        except HTTPException:
            # Re-raise HTTP exceptions (validation errors)
            raise
        except SQLAlchemyError as e:
            # Catch database errors
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to authenticate user",
            ) from e
