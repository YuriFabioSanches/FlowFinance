from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.schemas.user import User as UserSchema, UserUpdate
from src.services.auth_service import get_current_user
from src.repositories.user_repository import UserRepository
from src.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_user)):
    try:
        user = await current_user
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while fetching user: {e}")

@router.put("/me", response_model=UserSchema)
async def update_users_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        user = await current_user
        user_repo = UserRepository(db)
        updated_user = user_repo.update_user(user.id, user_update)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while updating user: {e}") 