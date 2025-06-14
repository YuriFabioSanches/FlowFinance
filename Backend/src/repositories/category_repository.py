from sqlalchemy.orm import Session
from src.models.category import Category
from src.schemas.category import CategoryCreate, CategoryUpdate
from typing import List, Optional

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, category: CategoryCreate) -> Category:
        db_category = Category(**category.dict(), user_id=user_id)
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def get(self, user_id: int, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter_by(id=category_id, user_id=user_id).first()

    def get_all(self, user_id: int) -> List[Category]:
        return self.db.query(Category).filter_by(user_id=user_id).all()

    def update(self, user_id: int, category_id: int, category: CategoryUpdate) -> Optional[Category]:
        db_category = self.get(user_id, category_id)
        if not db_category:
            return None
        for key, value in category.dict(exclude_unset=True).items():
            setattr(db_category, key, value)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def delete(self, user_id: int, category_id: int) -> bool:
        db_category = self.get(user_id, category_id)
        if not db_category:
            return False
        self.db.delete(db_category)
        self.db.commit()
        return True 