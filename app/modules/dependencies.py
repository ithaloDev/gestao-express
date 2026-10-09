from fastapi import Depends
from sqlmodel import Session
from app.core.database import get_session

from app.modules.transactions.unit import UnitOfWork
from .transactions.service import TransactionService, CategoryService

def get_uow(session: Session = Depends(get_session)) -> UnitOfWork:
    return UnitOfWork(session=session)

def get_transaction_service(uow: UnitOfWork = Depends(get_uow)) -> TransactionService:
    return TransactionService(uow=uow)

def get_category_service(uow: UnitOfWork = Depends(get_uow)) -> CategoryService:
    return CategoryService(uow=uow)