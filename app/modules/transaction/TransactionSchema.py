from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .TransactionEnums import TransactionTypeEnum, TransactionStatusEnum

class TransactionCreate(BaseModel):
    description: str
    amount: Decimal
    transaction_type: TransactionTypeEnum
    status: TransactionStatusEnum
    category_id: UUID
    date: datetime

class TransactionResponse(BaseModel):
    id: Optional[UUID]
    description: str 
    amount: Decimal
    transaction_type: TransactionTypeEnum
    status: TransactionStatusEnum
    category_id: UUID
    date: datetime
    updated_at: datetime
    
class TranscationUpdate(BaseModel):
    id: Optional[UUID]
    description: str
    amount: Decimal
    transaction_type: TransactionTypeEnum
    status: TransactionStatusEnum
    category_id: UUID
    date: datetime