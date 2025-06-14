from sqlalchemy.orm import Session

from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from src.core.security import get_password_hash


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create(self, user: UserCreate) -> User:
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=get_password_hash(user.password)
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user_update: UserUpdate) -> User | None:
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None

        update_data = user_update.dict(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data["password"])
            del update_data["password"]

        for key, value in update_data.items():
            setattr(db_user, key, value)

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user 