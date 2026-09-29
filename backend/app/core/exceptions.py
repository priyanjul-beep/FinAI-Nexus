class FinAINexusException(Exception):
    """Base exception for FinAI Nexus."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class SecurityException(FinAINexusException):
    def __init__(self, message: str):
        super().__init__(message, code="SECURITY_VIOLATION", status_code=400)


class SQLValidationException(FinAINexusException):
    def __init__(self, message: str):
        super().__init__(message, code="SQL_VALIDATION_ERROR", status_code=400)


class DocumentProcessingException(FinAINexusException):
    def __init__(self, message: str):
        super().__init__(message, code="DOCUMENT_PROCESSING_ERROR", status_code=422)


class AuthenticationException(FinAINexusException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="UNAUTHORIZED", status_code=401)


class AuthorizationException(FinAINexusException):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, code="FORBIDDEN", status_code=403)
