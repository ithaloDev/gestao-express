from decimal import Decimal
from datetime import datetime, date
from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel

class TransactionBaseModel(SQLModel):
    id: Optional[UUID]
    description: str
    amount: Decimal
    category_id: UUID
    
    transaction_type: str
    transaction_date: Optional[date]
    
    created_at: datetime
    updated_at: datetime
    
    
class CategoryBaseModel(SQLModel):
    id: Optional[UUID]
    name: str
    created_at: datetime


