from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, Column
from datetime import date, datetime, timezone
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from .BaseModel import TransactionBaseModel
from app.modules.transactions.enum import ValidationLimits, MoneyDefaults
import sqlalchemy as sa

if TYPE_CHECKING:
    from .CategoryModel import Category

class Transaction(TransactionBaseModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    
    description: str = Field(min_length=ValidationLimits.TRANSACTION_DESCRIPTION_MIN, max_length=ValidationLimits.TRANSACTION_DESCRIPTION_MAX, nullable=False)
    
    amount: Decimal = Field(
        default=MoneyDefaults.DEFAULT_AMOUNT, 
        ge=float(MoneyDefaults.MIN_AMOUNT), 
        decimal_places=MoneyDefaults.DECIMAL_PLACES, 
        max_digits=MoneyDefaults.TOTAL_DIGITS, 
        
        sa_column=Column(
            sa.Numeric(
                precision=MoneyDefaults.TOTAL_DIGITS, 
                scale=MoneyDefaults.DECIMAL_PLACES
            ),
            nullable=False,
            default=MoneyDefaults.DEFAULT_AMOUNT
        ))
    
    category_id: UUID = Field(foreign_key="category.id", nullable=False, ondelete="RESTRICT")
    
    transaction_type: str = Field(max_length=10, nullable=False)
    transaction_date: Optional[date] = Field(default_factory=date.today, nullable=False)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)})
    
    category: "Category" = Relationship(back_populates="transactions")