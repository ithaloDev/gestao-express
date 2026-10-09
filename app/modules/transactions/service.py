from typing import Sequence
from datetime import date
from uuid import UUID
from app.modules.transactions.enum import TransactionTypeEnum
from app.modules.transactions.exception import NotFoundException, BadRequestException
from app.modules.transactions.unit import UnitOfWork
from app.modules.transactions.schema import (
    BalanceSummaryResponse,
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    CategoryResponse, 
    CategoryWithTransactionsResponse,
    DeleteAllResponse
)

class CategoryService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_all(self) -> Sequence[CategoryResponse]:
        with self.uow:
            categories = self.uow.category_repo.get_all()
            return [CategoryResponse.model_validate(category) for category in categories]

    def get_by_id(self, category_id: UUID) -> CategoryWithTransactionsResponse:
        with self.uow:
            category = self.uow.category_repo.get_by_id(category_id)
            if not category:
                raise NotFoundException("Categoria não encontrada", {
                    "category_id": category_id
                })
            return CategoryWithTransactionsResponse.model_validate(category)

    def delete_category(self, category_id: UUID) -> DeleteAllResponse:
        with self.uow:
            category = self.uow.category_repo.get_by_id(category_id)
            if not category:
                raise NotFoundException("Categoria não encontrada", {
                    "category_id" : category_id
                })
            
            # Verifica se há transações vinculadas na memória carregada
            if len(category.transactions) > 0:
                raise BadRequestException("Não é possível deletar uma categoria que possui transações vinculadas.", {
                    "transactions": [TransactionResponse.model_validate(transaction).model_dump() for transaction in category.transactions]
                })
            
            category_name = category.name
                
            self.uow.category_repo.delete(category)
            self.uow.commit()
            
            return DeleteAllResponse(
                message="Categoria deletada com sucesso",
                details={"Categoria deletada": category_name}
            )

    def delete_all_unused(self) -> DeleteAllResponse:
        with self.uow:
            total = self.uow.category_repo.delete_all_unused()
            self.uow.commit()
            
            if total > 0:
                message = "Categoria deletada com sucesso"
            else:
                message = "Nenhuma categoria não utilizada foi encontrada."
            
            return DeleteAllResponse(
                message=message,
                details={"deleted_categories": total}
            )

class TransactionService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        
    def create_transaction(self, data: TransactionCreate) -> TransactionResponse:
        with self.uow:
            category = self.uow.category_repo.get_or_create(data.category_name)
            
            transaction_dict = data.model_dump(exclude={"category_name"})
            transaction_dict.update({"category_id": category.id})
            
            transaction_model = self.uow.transaction_repo.convert_dto_to_model(transaction_dict)
            
            saved_transaction = self.uow.transaction_repo.create(transaction_model)
            
            self.uow.commit()
            self.uow.refresh(saved_transaction)
            
            return TransactionResponse.model_validate(saved_transaction)
    
    def update_transaction(self, transaction_id: UUID, modified_transaction: TransactionUpdate) -> TransactionResponse:
        with self.uow:
            transaction = self.uow.transaction_repo.get_by_id(transaction_id)
            
            if not transaction: 
                raise NotFoundException("Transação não encontrada", {
                    "transaction_id" : transaction_id
                })
            
            update_data = modified_transaction.model_dump(exclude_unset=True)
                    
            if "category_name" in update_data:
                category_name = update_data.pop("category_name") 
                
                current_category_name = transaction.category.name if transaction.category else None
                
                if category_name != current_category_name:
                    
                    category = self.uow.category_repo.get_or_create(category_name)
                    update_data.update({"category_id" : category.id})
                
            updated_transaction_model = self.uow.transaction_repo.update(transaction, update_data)
            
            self.uow.commit()
            self.uow.refresh(updated_transaction_model)
            
            return TransactionResponse.model_validate(updated_transaction_model)
            
    def delete_transaction(self, transaction_id: UUID) -> DeleteAllResponse:
        with self.uow:
            transaction = self.uow.transaction_repo.get_by_id(transaction_id)
            
            if not transaction:
                raise NotFoundException("Transação não encontrada", {
                    "transaction_id": transaction_id
                })

            self.uow.transaction_repo.delete(transaction)
            
            self.uow.commit()
            
            return DeleteAllResponse(
                message="Transação deletada com sucesso",
                details={"transaction_id": transaction_id}
            )
        
    def delete_transactions_by_date(self, target_date: date) -> DeleteAllResponse:
        with self.uow:
            self.uow.transaction_repo.delete_by_date(target_date)
            self.uow.commit()
            
            return DeleteAllResponse(
                message=f"Transações da data {target_date} deletadas com sucesso."
            )
            
    def get_all(self) -> Sequence[TransactionResponse]:
        with self.uow:
            transactions = self.uow.transaction_repo.get_all()
            return [TransactionResponse.model_validate(transaction) for transaction in transactions]

    def get_balance_summary(self) -> BalanceSummaryResponse:
        with self.uow:
            renda = self.uow.transaction_repo.get_total_by_type(TransactionTypeEnum.INCOME)
            despesa = self.uow.transaction_repo.get_total_by_type(TransactionTypeEnum.EXPENSE)
            saldo_atual = renda - despesa

            return BalanceSummaryResponse(
                saldo_atual=saldo_atual,
                despesa=despesa,
                renda=renda
            )