from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .TransactionEnums import TransactionTypeEnum, TransactionStatusEnum

class CategoryBase(BaseModel):
    id: Optional[UUID]
    name: str
    transactions: List[TransactionBase]

class TransactionBase(BaseModel):
    id: Optional[UUID]
    description: str 
    amount: Decimal
    transaction_type: TransactionTypeEnum
    status: TransactionStatusEnum
    category: UUID
    date: datetime
    updated_at: datetime
    category_rel: CategoryBase

class TransactionCreate(BaseModel):
    description: str
    amount: Decimal
    transaction_type: TransactionTypeEnum
    status: TransactionStatusEnum
    category: UUID
    date: datetime

class TransactionResponse(BaseModel):
    id: Optional[int]
    description: str 
    amount: Decimal
    transaction_type: TransactionTypeEnum
    status: TransactionStatusEnum
    category: UUID
    date: datetime
    updated_at: datetime
    
class TranscationUpdate(BaseModel):
    id: Optional[UUID]
    description: str
    amount: Decimal
    transaction_type: TransactionTypeEnum
    status: TransactionStatusEnum
    category: UUID
    date: datetime