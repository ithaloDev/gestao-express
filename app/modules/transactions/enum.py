from enum import Enum
from decimal import Decimal

class TransactionTypeEnum(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"
    
class ValidationLimits:
    CATEGORY_NAME_MAX = 100
    CATEGORY_NAME_MIN = 3
    TRANSACTION_DESCRIPTION_MAX = 100
    TRANSACTION_DESCRIPTION_MIN = 3
    TRANSACTION_TYPE_MAX = 10
    USER_NAME_MAX = 255

class MoneyDefaults:
    DEFAULT_AMOUNT = Decimal("0.00")
    MIN_AMOUNT = Decimal("0.00")
    DECIMAL_PLACES = 2
    TOTAL_DIGITS = 20