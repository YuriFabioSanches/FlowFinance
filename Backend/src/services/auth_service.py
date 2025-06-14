from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.database import get_db
from src.core.security import verify_password, create_access_token
from src.repositories.user_repository import UserRepository
from src.schemas.user import TokenData, UserCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.user_repository = UserRepository(db)

    def authenticate_user(self, username: str, password: str):
        user = self.user_repository.get_by_username(username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(
            data=data, expires_delta=access_token_expires
        )

    async def get_current_user(
        self,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        
        user_repository = UserRepository(db)
        user = user_repository.get_by_username(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    def register_user(self, user: UserCreate):
        db_user = self.user_repository.get_by_email(email=user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        db_user = self.user_repository.get_by_username(username=user.username)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        return self.user_repository.create(user=user)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return AuthService(db).get_current_user(token=token, db=db) 