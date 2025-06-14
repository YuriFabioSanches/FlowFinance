from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.core.database import get_db
from src.services.auth_service import get_current_user
from src.services.account_service import AccountService
from src.schemas.account import AccountCreate, AccountUpdate, AccountInDB
from src.models.user import User

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/", response_model=AccountInDB, status_code=status.HTTP_201_CREATED)
async def create_account(
    account: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = AccountService(db)
        return service.create_account(user.id, account)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while creating account: {e}")

@router.get("/", response_model=List[AccountInDB])
async def list_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = AccountService(db)
        return service.get_accounts(user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while listing accounts: {e}")

@router.get("/{account_id}", response_model=AccountInDB)
async def get_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = AccountService(db)
        account = service.get_account(user.id, account_id)
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        return account
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while fetching account: {e}")

@router.put("/{account_id}", response_model=AccountInDB)
async def update_account(
    account_id: int,
    account: AccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = AccountService(db)
        updated = service.update_account(user.id, account_id, account)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        return updated
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while updating account: {e}")

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = AccountService(db)
        deleted = service.delete_account(user.id, account_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        return None
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while deleting account: {e}") 