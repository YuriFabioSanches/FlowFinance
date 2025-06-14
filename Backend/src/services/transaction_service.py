from sqlalchemy.orm import Session
from src.repositories.transaction_repository import TransactionRepository
from src.schemas.transaction import TransactionCreate, TransactionUpdate
from src.models.transaction import Transaction
from typing import List, Optional
import json
import zipfile
import os
from datetime import datetime

class TransactionService:
    def __init__(self, db: Session):
        self.repository = TransactionRepository(db)

    def create_transaction(self, user_id: int, transaction: TransactionCreate) -> Transaction:
        return self.repository.create(user_id, transaction)

    def get_transaction(self, user_id: int, transaction_id: int) -> Optional[Transaction]:
        return self.repository.get(user_id, transaction_id)

    def get_transactions(self, user_id: int) -> List[Transaction]:
        return self.repository.get_all(user_id)

    def update_transaction(self, user_id: int, transaction_id: int, transaction: TransactionUpdate) -> Optional[Transaction]:
        return self.repository.update(user_id, transaction_id, transaction)

    def delete_transaction(self, user_id: int, transaction_id: int) -> bool:
        return self.repository.delete(user_id, transaction_id)

    def export_transactions(self, user_id: int) -> str:
        transactions = self.get_transactions(user_id)
        
        # Convert transactions to JSON-serializable format
        transactions_data = []
        for transaction in transactions:
            transaction_dict = {
                "id": transaction.id,
                "user_id": transaction.user_id,
                "category_id": transaction.category_id,
                "account_id": transaction.account_id,
                "amount": transaction.amount,
                "transaction_type": transaction.transaction_type,
                "description": transaction.description,
                "source": transaction.source,
                "date": transaction.date.isoformat()
            }
            transactions_data.append(transaction_dict)

        # Create a temporary directory if it doesn't exist
        os.makedirs("temp", exist_ok=True)
        
        # Generate unique filename with timestamp
        current_date = datetime.now().strftime("%Y%m%d")
        json_filename = f"temp/Transactions_{current_date}.json"
        zip_filename = f"temp/Transactions_{current_date}.zip"

        # Write transactions to JSON file
        with open(json_filename, 'w') as f:
            json.dump(transactions_data, f, indent=4)

        # Create zip file
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write(json_filename, os.path.basename(json_filename))

        # Remove the JSON file after zipping
        os.remove(json_filename)

        return zip_filename

    def import_transactions(self, user_id: int, file_path: str) -> List[Transaction]:
        try:
            with open(file_path, 'r') as f:
                transactions_data = json.load(f)

            imported_transactions = []
            for transaction_data in transactions_data:
                # Create a TransactionCreate object from the data
                transaction = TransactionCreate(
                    amount=transaction_data["amount"],
                    transaction_type=transaction_data["transaction_type"],
                    description=transaction_data.get("description"),
                    source=transaction_data.get("source"),
                    category_id=transaction_data.get("category_id"),
                    account_id=transaction_data.get("account_id"),
                    date=datetime.fromisoformat(transaction_data["date"]).date()
                )
                
                # Create the transaction in the database
                created_transaction = self.create_transaction(user_id, transaction)
                imported_transactions.append(created_transaction)

            return imported_transactions
        except Exception as e:
            raise Exception(f"Error importing transactions: {str(e)}") 