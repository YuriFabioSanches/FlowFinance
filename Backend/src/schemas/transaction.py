from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum

class TransactionType(str, Enum):
    EXPENSE = "expense"
    REVENUE = "revenue"

class TransactionBase(BaseModel):
    amount: float
    transaction_type: TransactionType
    description: Optional[str] = None
    source: Optional[str] = None
    category_id: Optional[int] = None
    account_id: Optional[int] = None
    date: date

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class TransactionInDB(TransactionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True 