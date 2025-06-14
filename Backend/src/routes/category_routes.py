from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.core.database import get_db
from src.services.auth_service import get_current_user
from src.services.category_service import CategoryService
from src.schemas.category import CategoryCreate, CategoryUpdate, CategoryInDB
from src.models.user import User

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("/", response_model=CategoryInDB, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = CategoryService(db)
        return service.create_category(user.id, category)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while creating category: {e}")

@router.get("/", response_model=List[CategoryInDB])
async def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = CategoryService(db)
        return service.get_categories(user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while listing categories: {e}")

@router.get("/{category_id}", response_model=CategoryInDB)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = CategoryService(db)
        category = service.get_category(user.id, category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return category
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while fetching category: {e}")

@router.put("/{category_id}", response_model=CategoryInDB)
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = CategoryService(db)
        updated = service.update_category(user.id, category_id, category)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return updated
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while updating category: {e}")

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = CategoryService(db)
        deleted = service.delete_category(user.id, category_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return None
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while deleting category: {e}") 