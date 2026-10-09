from typing import Optional, Sequence
from datetime import date
from decimal import Decimal
from uuid import UUID
from sqlmodel import Session, select, func, desc
from sqlalchemy.orm import joinedload
from app.modules.transactions.entity.TransactionModel import Transaction
from app.modules.transactions.enum import TransactionTypeEnum
from app.modules.transactions.repository.BaseRepo import TransactionBase

class TransactionRepository(TransactionBase):
    def __init__(self, session: Session):
        self.session = session
        
    def _save(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        self.session.flush()
        return transaction

    def create(self, transaction: Transaction) -> Transaction:
        return self._save(transaction)

    def convert_dto_to_model(self, data: dict) -> Transaction:
        return Transaction.model_validate(data)

    def get_by_id(self, id: UUID) -> Optional[Transaction]:
        return self.session.get(Transaction, id)

    def get_all(self) -> Sequence[Transaction]:
        stmt = (
            select(Transaction)
            .options(joinedload(Transaction.category))  # type: ignore
            .order_by(desc(Transaction.updated_at))
        )
        return self.session.exec(stmt).all()

    def update(self, transaction: Transaction, update_data: dict) -> Transaction:
        transaction.sqlmodel_update(update_data)
        return self._save(transaction)

    def delete(self, transaction: Transaction) -> None:
        self.session.delete(transaction)
        
    def delete_by_date(self, target_date: date) -> None:
        stmt = select(Transaction).where(Transaction.transaction_date == target_date)
        transactions = self.session.exec(stmt).all()
        
        for transaction in transactions: self.session.delete(transaction)

    def get_total_by_type(self, t_type: TransactionTypeEnum) -> Decimal:
        stmt = select(func.sum(Transaction.amount)).where(Transaction.transaction_type == t_type)
        total = self.session.exec(stmt).first()
        return Decimal(total) if total else Decimal("0.00")
    
    def get_total_by_category(self, category_id: UUID) -> Decimal:
        stmt = select(func.sum(Transaction.amount)).where(Transaction.category_id == category_id)
        result = self.session.exec(stmt).first()
        return Decimal(result) if result else Decimal("0.00")
