from typing import Dict, Optional, Any

class DomainException(Exception):
    def __init__(self,message: str, status_code: int, error_code: str, context: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.context = context or {}
        super().__init__(self.message)

class NotFoundException(DomainException):
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=404,
            error_code="RESOURCE_NOT_FOUND",
            context=context
        )

class BadRequestException(DomainException):
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=400,
            error_code="BAD_REQUEST",
            context=context
        )