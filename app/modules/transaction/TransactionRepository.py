from typing import List, Optional, Annotated, Dict
from uuid import UUID
from sqlmodel import Session, select, SQLModel
from .TransactionModel import Category, Transaction

class BaseRepository[ModelType: SQLModel]:
    def __init__(self, model: type[ModelType], session: Session):
        self.model = model
        self.session = session
        
    def _save(self, instance: ModelType) -> ModelType:
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)

        return instance
    
    def create(self, instance: ModelType) -> ModelType:
        return self._save(instance)
    
    def find_by_id(self, id: UUID) -> ModelType | None:
        return self.session.get(self.model, id)
        
    def get_all(self,):
        query = select(self.model)
        return self.session.exec(query).all()
    
class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self, session: Session):
        super().__init__(Transaction, session)
        
    def find_by_id(self, id: UUID):
        return self.session.get(Transaction, id)
    
    def update(self, id: UUID, update_data: dict):
        transaction = self.find_by_id(id)
        
        if not transaction: return False
        
        transaction.sqlmodel_update(update_data)

        for key, value in update_data.items():
            setattr(transaction, key, value)        
        
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        
        return transaction
    
    def delete(self, id: UUID):
        transaction = self.find_by_id(id)
        
        if not transaction: return False
        
        self.session.delete(transaction)
        self.session.commit()
        
        return True
    
class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: Session):
        super().__init__(Category, session)
    
    def find_by_id(self, id: UUID):
        category = self.session.get(Category, id)
        
        return category
    
    def delete(self, id: UUID):
        category = self.find_by_id(id)
        
        if not category: return False
        
        self.session.delete(category)
        self.session.commit()
        
        return True
        