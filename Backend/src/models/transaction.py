from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.core.database import Base
import enum

class TransactionType(enum.Enum):
    EXPENSE = "expense"
    REVENUE = "revenue"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    source = Column(String, nullable=True)
    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, category_id={self.category_id}, amount={self.amount}, transaction_type={self.transaction_type}, description={self.description}, source={self.source}, date={self.date})>" 