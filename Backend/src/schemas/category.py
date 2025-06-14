from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None

class CategoryInDB(CategoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True 