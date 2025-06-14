from sqlalchemy.orm import Session
from src.models.account import Account
from src.schemas.account import AccountCreate, AccountUpdate
from typing import List, Optional

class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, account: AccountCreate) -> Account:
        db_account = Account(**account.dict(), user_id=user_id)
        self.db.add(db_account)
        self.db.commit()
        self.db.refresh(db_account)
        return db_account

    def get(self, user_id: int, account_id: int) -> Optional[Account]:
        return self.db.query(Account).filter_by(id=account_id, user_id=user_id).first()

    def get_all(self, user_id: int) -> List[Account]:
        return self.db.query(Account).filter_by(user_id=user_id).all()

    def update(self, user_id: int, account_id: int, account: AccountUpdate) -> Optional[Account]:
        db_account = self.get(user_id, account_id)
        if not db_account:
            return None
        for key, value in account.dict(exclude_unset=True).items():
            setattr(db_account, key, value)
        self.db.commit()
        self.db.refresh(db_account)
        return db_account

    def delete(self, user_id: int, account_id: int) -> bool:
        db_account = self.get(user_id, account_id)
        if not db_account:
            return False
        self.db.delete(db_account)
        self.db.commit()
        return True 