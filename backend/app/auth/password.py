from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Centralized Argon2 configuration for production-grade hashing
_hasher = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4, hash_len=32, salt_len=16)


def hash_password(password: str) -> str:
    """Hash a password using Argon2.

    Args:
        password: Plain text password to hash.

    Returns:
        Argon2 hash string.
    """
    return _hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its Argon2 hash.

    Args:
        password: Plain text password to verify.
        hashed_password: Argon2 hash to check against.

    Returns:
        True if password matches, False otherwise.
    """
    try:
        _hasher.verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        return False


def password_needs_rehash(hashed_password: str) -> bool:
    """Check if a password hash needs to be rehashed with current parameters.

    Use this to trigger password updates on login if hashing parameters have changed.

    Args:
        hashed_password: Argon2 hash to check.

    Returns:
        True if the hash was created with different parameters, False otherwise.
    """
    return _hasher.check_needs_rehash(hashed_password)
