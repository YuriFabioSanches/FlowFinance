from sqlalchemy.orm import Session
from src.repositories.category_repository import CategoryRepository
from src.schemas.category import CategoryCreate, CategoryUpdate
from src.models.category import Category
from typing import List, Optional

class CategoryService:
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def create_category(self, user_id: int, category: CategoryCreate) -> Category:
        return self.repository.create(user_id, category)

    def get_category(self, user_id: int, category_id: int) -> Optional[Category]:
        return self.repository.get(user_id, category_id)

    def get_categories(self, user_id: int) -> List[Category]:
        return self.repository.get_all(user_id)

    def update_category(self, user_id: int, category_id: int, category: CategoryUpdate) -> Optional[Category]:
        return self.repository.update(user_id, category_id, category)

    def delete_category(self, user_id: int, category_id: int) -> bool:
        return self.repository.delete(user_id, category_id) 