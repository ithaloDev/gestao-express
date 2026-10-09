from typing import Optional, Sequence
from uuid import UUID
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select, col
from app.modules.transactions.entity.CategoryModel import Category
from app.modules.transactions.entity.TransactionModel import Transaction
from app.modules.transactions.repository.BaseRepo import CategoryBase

class CategoryRepository(CategoryBase):
    def __init__(self, session: Session):
        self.session = session
        
    def _save(self, category: Category) -> Category:
        self.session.add(category)
        self.session.flush() # Atribui o ID gerado sem encerrar a transação
        return category
    
    def get_or_create(self, name: str) -> Category:
        category = self.get_by_name(name)
        if category:
            return category
        
        new_category = Category(name=name)
        
        return self._save(new_category)

    # def get_by_id(self, category_id: UUID) -> Optional[Category]:
    #     return self.session.get(Category, category_id)

    def get_all(self) -> Sequence[Category]:
        stmt = select(Category)
        return self.session.exec(stmt).all()

    def get_by_name(self, name: str) -> Optional[Category]:
        stmt = select(Category).where(Category.name == name)
        return self.session.exec(stmt).first()

    def create(self, category: Category) -> Category:
        return self._save(category)

    def delete(self, category: Category) -> None:
        self.session.delete(category)
        
    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        # Utilizei o type: ignore por causa do error de tipagem do proprio python.
        # Sqlmodel faz a conversão automaticamente para chave do atributo modelo
        stmt = (
            select(Category)
            .where(Category.id == category_id)
            .options(joinedload(Category.transactions)) # type: ignore
        )
        return self.session.exec(stmt).first()
    
    def delete_all_unused(self) -> int:
        # pegar todos os ids de categorias nas transações vinculadas e distantas
        stmt = select(Transaction.category_id).distinct()
        transactions_ids = self.session.exec(stmt).all()
        
        # Seleciona categorias que o ID da Categoria NÃO esteja presente na lista de category_id na transação
        stmt = select(Category).where(col(Category.id).not_in(transactions_ids))
        categories = self.session.exec(stmt).all()
        
        # Conta todas categorias filtradas
        total_deleted = len(categories)
        
        for category in categories: self.session.delete(category)
            
        return total_deleted