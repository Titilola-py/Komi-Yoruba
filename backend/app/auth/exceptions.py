"""Custom exceptions for authentication operations.

Future implementation:
- Structured error responses for authentication failures
- Consistent HTTP status codes and error messages
- Exception handling across auth endpoints
"""

from fastapi import HTTPException, status


class AuthenticationError(HTTPException):
    """Base exception for authentication-related errors.

    Future implementation will extend this with specific error types:
    - InvalidCredentialsError: Wrong email/password
    - TokenExpiredError: JWT token has expired
    - InvalidTokenError: JWT token is invalid/tampered
    - UserNotFoundError: User does not exist
    - UserInactiveError: User account is disabled
    """

    def __init__(self, detail: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        """Initialize authentication error.

        Args:
            detail: Error message.
            status_code: HTTP status code (default 401 Unauthorized).
        """
        super().__init__(status_code=status_code, detail=detail)


# Placeholder for specific exception subclasses
# These will be implemented as features are added
