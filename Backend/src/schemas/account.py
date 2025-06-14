from pydantic import BaseModel
from typing import Optional

class AccountBase(BaseModel):
    name: str
    initial_balance: float = 0.0

class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountBase):
    name: Optional[str] = None
    initial_balance: Optional[float] = None

class AccountInDB(AccountBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True 