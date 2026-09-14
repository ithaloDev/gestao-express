from enum import Enum

class TransactionTypeEnum(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionStatusEnum(str, Enum):
    COMPLETED = "completed"
    PENDING = "peding"