"""JWT token generation and validation for authentication.

Handles creation of access tokens using HS256 signing.
Token claims include:
  - sub: User ID (as string)
  - email: User email
  - iat: Issued-at timestamp
  - exp: Token expiration timestamp

Token verification will be implemented in the dependencies module.
"""

from datetime import datetime, timedelta, timezone
from os import getenv

from jose import jwt

# Load JWT configuration from environment
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set. Add it to .env file.")


def create_access_token(user_id: int, email: str, expires_delta_minutes: int | None = None) -> str:
    """Generate a JWT access token for a user.

    Token contains:
      - sub: User ID (subject claim)
      - email: User email address
      - iat: Issued-at timestamp
      - exp: Token expiration timestamp

    Args:
        user_id: The user's ID from the database.
        email: The user's email address.
        expires_delta_minutes: Optional token lifetime in minutes.
                               Defaults to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        Encoded JWT token as a string.

    Raises:
        ValueError: If SECRET_KEY is not configured.
    """
    # Use provided expiration or configured default
    expire_minutes = (
        expires_delta_minutes
        if expires_delta_minutes is not None
        else ACCESS_TOKEN_EXPIRE_MINUTES
    )

    issued_at = datetime.now(timezone.utc)

    # Calculate expiration time (UTC)
    expire_time = issued_at + timedelta(minutes=expire_minutes)

    # Prepare token claims (JWT spec compliant)
    to_encode = {
        "sub": str(user_id),
        "email": email,
        "iat": issued_at,
        "exp": expire_time,
    }

    # Encode and sign the JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
