from uuid import UUID
from typing import Sequence, Annotated
from datetime import date
from fastapi import APIRouter, Depends, status
from app.modules.transactions.service import TransactionService
from app.modules.dependencies import get_transaction_service

from app.modules.transactions.schema import (
    TransactionCreate, 
    TransactionUpdate, 
    TransactionResponse, 
    DeleteAllResponse,
    BalanceSummaryResponse
)

TransactionRouter = APIRouter(prefix="/transactions", tags=["Transactions"])

@TransactionRouter.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    data: TransactionCreate,
    service: Annotated[TransactionService, Depends(get_transaction_service)]
):
    return service.create_transaction(data)

@TransactionRouter.get("/", response_model=Sequence[TransactionResponse])
def get_all_transactions(
    service: TransactionService = Depends(get_transaction_service)
):
    return service.get_all()

@TransactionRouter.get("/summary", response_model=BalanceSummaryResponse)
def get_balance_summary(
    service: TransactionService = Depends(get_transaction_service)
):
    return service.get_balance_summary()

@TransactionRouter.patch("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: UUID,
    data: TransactionUpdate,
    service: TransactionService = Depends(get_transaction_service)
):
    return service.update_transaction(transaction_id, data)

@TransactionRouter.delete("/{transaction_id}", response_model=DeleteAllResponse, status_code=status.HTTP_200_OK)
def delete_transaction(
    transaction_id: UUID,
    service: TransactionService = Depends(get_transaction_service)
):
    return service.delete_transaction(transaction_id)

@TransactionRouter.delete("/delete/all", response_model=DeleteAllResponse, status_code=status.HTTP_200_OK)
def delete_transactions_by_date(
    data: date,
    service: TransactionService = Depends(get_transaction_service)
):
    return service.delete_transactions_by_date(data)