from typing import List, Optional
from sqlmodel import Session, select
from .TransactionSchema import TransactionCreate, TransactionResponse
from .TransactionModel import Category, Transaction

class TransactionRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def create(self, transaction: TransactionCreate):
        self.session.add(transaction)
        self.session.commit()
        
    def findById(self, id: str):
        transaction_data = self.session.get(Transaction, id)
        
        return transaction_data
