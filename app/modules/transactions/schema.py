from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator, field_serializer, model_validator
from app.modules.transactions.enum import TransactionTypeEnum, ValidationLimits, MoneyDefaults

# --- CATEGORY SCHEMAS ---

class CategoryBase(BaseModel):
    name: str
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        return value.lower().strip()

class CategoryCreate(CategoryBase):
   name: str = Field(
        min_length=ValidationLimits.CATEGORY_NAME_MIN, 
        max_length=ValidationLimits.CATEGORY_NAME_MAX, 
        description=f"O nome da categoria deve ter entre {ValidationLimits.CATEGORY_NAME_MIN} e {ValidationLimits.CATEGORY_NAME_MAX} caracteres"
    )

class CategoryResponse(CategoryBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)

class CategoryWithTransactionsResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    transactions: list[TransactionResponse] = []

    model_config = ConfigDict(from_attributes=True)

# --- TRANSACTION SCHEMAS ---

class TransactionBase(BaseModel):
    amount: Decimal
    description: str
    category_name: str
    transaction_type: str
    
    @field_validator('category_name')
    @classmethod
    def validate_category_name(cls, value: str) -> str:
        return value.lower().strip()
    
    @field_serializer('amount')
    def serialize_amount(self, amount: Decimal) -> str:
        return f"{amount:.2f}"
    
    @field_validator('transaction_type')
    @classmethod
    def validate_transaction_type(cls, value: str) -> str:
        if value.lower() not in [TransactionTypeEnum.INCOME, TransactionTypeEnum.EXPENSE]:
            raise ValueError("Selecione um tipo de transação válido (INCOME ou EXPENSE)")
        return value.lower()

class TransactionCreate(TransactionBase):
    amount: Decimal = Field(ge=MoneyDefaults.MIN_AMOUNT, description="O valor não pode ser menor do que zero")
    description: str = Field(min_length=ValidationLimits.TRANSACTION_DESCRIPTION_MIN, max_length=ValidationLimits.TRANSACTION_DESCRIPTION_MAX, description=f"A descrição deve ter entre {ValidationLimits.TRANSACTION_DESCRIPTION_MIN} e {ValidationLimits.TRANSACTION_DESCRIPTION_MAX} caracteres")
    
    transaction_date: Optional[date] = None

class TransactionResponse(BaseModel):
    id: UUID
    description: str
    amount: Decimal
    category_id: UUID 
    category_name: str
    transaction_type: str
    transaction_date: date
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
    @model_validator(mode="before")
    @classmethod
    def extrair_relacionamento_banco(cls, data):
        # Se os dados já forem um dicionário (ex: vindo de um teste ou JSON), apenas segue em frente
        if isinstance(data, dict):
            return data
            
        # Aqui está o pulo do gato: convertemos o modelo do banco em um dicionário Python puro.
        # O .model_dump() remove as travas do SQLModel que geravam o ValidationError!
        transaction_dict = data.model_dump()
        
        # Como o seu repository usou o joinedload, o objeto .category está vivo aqui na memória do Python
        if hasattr(data, "category") and data.category is not None:
            transaction_dict["category_name"] = data.category.name
        else:
            # Apenas para deixa elegante, mas é impossivel existir uma transação que não tenha um categoria vinculada sem derruba o servidor
            transaction_dict["category_name"] = "Sem Categoria"
            
        return transaction_dict
    
class TransactionUpdate(BaseModel):
    amount: Optional[Decimal] = Field(default=None, ge=MoneyDefaults.MIN_AMOUNT, description="O valor não pode ser menor do que zero")
    
    description: Optional[str] = Field(default=None, min_length=ValidationLimits.TRANSACTION_DESCRIPTION_MIN, max_length=ValidationLimits.TRANSACTION_DESCRIPTION_MAX, description=f"A descrição deve ter entre {ValidationLimits.TRANSACTION_DESCRIPTION_MIN} e {ValidationLimits.TRANSACTION_DESCRIPTION_MAX} caracteres")
    
    category_name: Optional[str] = None
    transaction_type: Optional[str] = None
    transaction_date: Optional[date] = None
    
    @field_validator('category_name')
    @classmethod
    def validate_category_name(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            return value.lower().strip()
        return value
        
    @field_validator('transaction_type')
    @classmethod
    def validate_transaction_type(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            if value.lower() not in [TransactionTypeEnum.INCOME, TransactionTypeEnum.EXPENSE]:
                raise ValueError("Selecione um tipo de transação válido (INCOME ou EXPENSE)")
            return value.lower()
        return value

# --- BALANCESUMMARY SCHEMA ---

class BalanceSummaryResponse(BaseModel):
    saldo_atual: Decimal
    despesa: Decimal
    renda: Decimal
    
    @field_serializer("saldo_atual", "despesa", "renda")
    def format_decimal(self, value: Decimal) -> str:
        return f"{value:.2f}"
    
    
# --- DELETEALL SCHEMA ---

class DeleteAllResponse(BaseModel):
    message: str
    details: dict = {}    