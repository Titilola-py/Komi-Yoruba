from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    """Data access layer for user persistence and queries.

    Transaction management is delegated to the service layer.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by email address.

        Args:
            email: Email to search for.

        Returns:
            User object if found, None otherwise.
        """
        return self.db.scalar(select(User).where(User.email == email))

    def get_by_username(self, username: str) -> User | None:
        """Retrieve a user by username.

        Args:
            username: Username to search for.

        Returns:
            User object if found, None otherwise.
        """
        return self.db.scalar(select(User).where(User.username == username))

    def create(self, user: User) -> User:
        """Add a user to the database and flush changes.

        Uses flush() to persist to the database without committing the transaction.
        The calling service layer is responsible for committing.

        Args:
            user: User object to create.

        Returns:
            User object with id and relationships populated.
        """
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user
