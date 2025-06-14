from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.core.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    initial_balance = Column(Float, nullable=False, default=0.0)

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account") 