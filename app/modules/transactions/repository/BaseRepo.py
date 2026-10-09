from abc import ABC, abstractmethod
from typing import Optional, Sequence
from datetime import date
from uuid import UUID
from app.modules.transactions.entity.CategoryModel import Category
from app.modules.transactions.entity.TransactionModel import Transaction
        
class TransactionBase(ABC):
    @abstractmethod
    def create(self, transaction: Transaction) -> Transaction: ...
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Transaction]: ...
    
    @abstractmethod
    def get_all(self) -> Sequence[Transaction]: ...
    
    @abstractmethod
    def delete(self, transaction: Transaction) -> None: ...
    
    @abstractmethod
    def update(self, transaction: Transaction, update_data: dict) -> Transaction: ...
    
    @abstractmethod
    def delete_by_date(self, target_date: date) -> None: ...


class CategoryBase(ABC):
    @abstractmethod
    def create(self, category: Category) -> Category: ...
    
    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Optional[Category]: ...
    
    @abstractmethod
    def get_all(self) -> Sequence[Category]: ...
    
    @abstractmethod
    def delete(self, category: Category) -> None: ...
    
    @abstractmethod
    def delete_all_unused(self) -> int: ...