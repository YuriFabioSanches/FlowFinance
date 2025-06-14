from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    transactions = relationship("Transaction", back_populates="user")
    categories = relationship("Category", back_populates="user")
    accounts = relationship("Account", back_populates="user") 