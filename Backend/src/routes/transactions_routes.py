from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from src.core.database import get_db
from src.services.auth_service import get_current_user
from src.services.transaction_service import TransactionService
from src.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionInDB
from src.models.user import User
import os
import shutil
from fastapi.responses import FileResponse

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionInDB, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = TransactionService(db)
        return service.create_transaction(user.id, transaction)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while creating transaction: {e}")

@router.get("/", response_model=List[TransactionInDB])
async def list_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = TransactionService(db)
        return service.get_transactions(user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while listing transactions: {e}")

@router.get("/export", response_class=FileResponse)
async def export_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = TransactionService(db)
        zip_file_path = service.export_transactions(user.id)
        
        # Return the zip file
        return FileResponse(
            path=zip_file_path,
            filename=os.path.basename(zip_file_path),
            media_type="application/zip"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while exporting transactions: {str(e)}"
        )

@router.get("/{transaction_id}", response_model=TransactionInDB)
async def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = TransactionService(db)
        transaction = service.get_transaction(user.id, transaction_id)
        if not transaction:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        return transaction
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while fetching transaction: {e}")

@router.put("/{transaction_id}", response_model=TransactionInDB)
async def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = TransactionService(db)
        updated = service.update_transaction(user.id, transaction_id, transaction)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        return updated
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while updating transaction: {e}")

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        service = TransactionService(db)
        deleted = service.delete_transaction(user.id, transaction_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        return None
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred while deleting transaction: {e}")

@router.post("/import", response_model=List[TransactionInDB])
async def import_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = await current_user
        
        # Create temp directory if it doesn't exist
        os.makedirs("temp", exist_ok=True)
        
        # Save uploaded file temporarily
        temp_file_path = f"temp/{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Import transactions
        service = TransactionService(db)
        imported_transactions = service.import_transactions(user.id, temp_file_path)
        
        # Clean up temporary file
        os.remove(temp_file_path)
        
        return imported_transactions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while importing transactions: {str(e)}"
        ) 