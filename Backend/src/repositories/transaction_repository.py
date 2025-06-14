from sqlalchemy.orm import Session
from src.models.transaction import Transaction, TransactionType
from src.schemas.transaction import TransactionCreate, TransactionUpdate
from typing import List, Optional

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, transaction: TransactionCreate) -> Transaction:
        db_transaction = Transaction(**transaction.dict(), user_id=user_id)
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction

    def get(self, user_id: int, transaction_id: int) -> Optional[Transaction]:
        return self.db.query(Transaction).filter_by(id=transaction_id, user_id=user_id).first()

    def get_all(self, user_id: int) -> List[Transaction]:
        return self.db.query(Transaction).filter_by(user_id=user_id).all()

    def update(self, user_id: int, transaction_id: int, transaction: TransactionUpdate) -> Optional[Transaction]:
        db_transaction = self.get(user_id, transaction_id)
        if not db_transaction:
            return None
        for key, value in transaction.dict().items():
            setattr(db_transaction, key, value)
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction

    def delete(self, user_id: int, transaction_id: int) -> bool:
        db_transaction = self.get(user_id, transaction_id)
        if not db_transaction:
            return False
        self.db.delete(db_transaction)
        self.db.commit()
        return True 