from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from typing import Optional, List
from decimal import Decimal
from datetime import datetime, timezone, date
from .TransactionEnums import TransactionTypeEnum, TransactionStatusEnum

class Category(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(max_length=80, nullable=False, unique=True)
    transactions: List["Transaction"] = Relationship(back_populates="category_rel")

class Transaction(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True, unique=True)
    description: str = Field(max_length=200, nullable=False)
    amount: Decimal = Field(default=0, nullable=False)
    transaction_type: TransactionTypeEnum = Field(default=TransactionTypeEnum.EXPENSE, nullable=False)
    status: TransactionStatusEnum = Field(default=TransactionStatusEnum.PENDING, nullable=False)
    
    category_id: UUID = Field(
        foreign_key="category.id", 
        nullable=False,
        ondelete="RESTRICT"  # Bloqueia a exclusão se houver transações vinculadas
    )
    
    date: date = Field(default=lambda: date.today)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )

    category_rel: Category  = Relationship(back_populates="transactions")
