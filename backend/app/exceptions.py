from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import Optional, Any
from app.logger import get_logger

logger = get_logger("exceptions")


class ErrorResponse(BaseModel):
    """Standard error response model"""
    status_code: int
    message: str
    detail: Optional[str] = None
    error_code: Optional[str] = None


class ValidationError(HTTPException):
    """Custom validation error"""
    def __init__(self, detail: str, error_code: str = "VALIDATION_ERROR"):
        logger.warning(f"Validation error: {detail} (code: {error_code})")
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
        self.error_code = error_code


class AuthenticationError(HTTPException):
    """Custom authentication error"""
    def __init__(self, detail: str = "Authentication failed", error_code: str = "AUTH_ERROR"):
        logger.warning(f"Authentication error: {detail} (code: {error_code})")
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )
        self.error_code = error_code


class AuthorizationError(HTTPException):
    """Custom authorization error"""
    def __init__(self, detail: str = "Access denied", error_code: str = "AUTHZ_ERROR"):
        logger.warning(f"Authorization error: {detail} (code: {error_code})")
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )
        self.error_code = error_code


class ResourceNotFoundError(HTTPException):
    """Custom resource not found error"""
    def __init__(self, resource: str, resource_id: Any, error_code: str = "NOT_FOUND"):
        detail = f"{resource} with id {resource_id} not found"
        logger.warning(f"Resource not found: {detail} (code: {error_code})")
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )
        self.error_code = error_code


class ConflictError(HTTPException):
    """Custom conflict error (e.g., duplicate resource)"""
    def __init__(self, detail: str, error_code: str = "CONFLICT"):
        logger.warning(f"Conflict error: {detail} (code: {error_code})")
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )
        self.error_code = error_code


class InsufficientStockError(HTTPException):
    """Custom error for insufficient stock"""
    def __init__(self, product_id: int, requested: int, available: int, error_code: str = "INSUFFICIENT_STOCK"):
        detail = f"Insufficient stock for product {product_id}. Requested: {requested}, Available: {available}"
        logger.warning(f"Insufficient stock: {detail} (code: {error_code})")
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
        self.error_code = error_code


class DatabaseError(HTTPException):
    """Custom database error"""
    def __init__(self, detail: str = "Database operation failed", error_code: str = "DB_ERROR"):
        logger.error(f"Database error: {detail} (code: {error_code})")
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
        self.error_code = error_code


class InternalServerError(HTTPException):
    """Custom internal server error"""
    def __init__(self, detail: str = "Internal server error", error_code: str = "INTERNAL_ERROR"):
        logger.error(f"Internal server error: {detail} (code: {error_code})")
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
        self.error_code = error_code
