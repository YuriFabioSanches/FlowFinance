from sqlalchemy.orm import Session
from src.repositories.account_repository import AccountRepository
from src.schemas.account import AccountCreate, AccountUpdate
from src.models.account import Account
from typing import List, Optional

class AccountService:
    def __init__(self, db: Session):
        self.repository = AccountRepository(db)

    def create_account(self, user_id: int, account: AccountCreate) -> Account:
        return self.repository.create(user_id, account)

    def get_account(self, user_id: int, account_id: int) -> Optional[Account]:
        return self.repository.get(user_id, account_id)

    def get_accounts(self, user_id: int) -> List[Account]:
        return self.repository.get_all(user_id)

    def update_account(self, user_id: int, account_id: int, account: AccountUpdate) -> Optional[Account]:
        return self.repository.update(user_id, account_id, account)

    def delete_account(self, user_id: int, account_id: int) -> bool:
        return self.repository.delete(user_id, account_id) 