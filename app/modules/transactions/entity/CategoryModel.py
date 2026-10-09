from uuid import UUID, uuid4
from sqlmodel import Field, Relationship
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from .BaseModel import CategoryBaseModel
from app.modules.transactions.enum import ValidationLimits

if TYPE_CHECKING:
    from .TransactionModel import Transaction

class Category(CategoryBaseModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(min_length=ValidationLimits.CATEGORY_NAME_MIN, max_length=ValidationLimits.CATEGORY_NAME_MAX, unique=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    transactions: List["Transaction"] = Relationship(back_populates="category")