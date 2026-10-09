from sqlmodel import Session
from app.modules.transactions.repository.CategoryRepo import CategoryRepository
from app.modules.transactions.repository.TransactionRepo import TransactionRepository

class UnitOfWork:
    def __init__(self, session: Session):
        self.session = session
    
    def __enter__(self):        
        self.transaction_repo = TransactionRepository(self.session)
        self.category_repo = CategoryRepository(self.session)
        return self
    
    def __exit__(self, exc_type, exc, traceback):
        if exc_type:
            self.session.rollback()
    
    def commit(self):
        self.session.commit()
    
    def rollback(self):
        self.session.rollback()
        
    def refresh(self, instance):
        self.session.refresh(instance)