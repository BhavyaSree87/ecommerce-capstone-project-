from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, List
from datetime import datetime

T = TypeVar('T')


class PaginationParams(BaseModel):
    
    page: int = Field(1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(20, ge=1, le=100, description="Number of items per page")


class PaginatedResponse(BaseModel, Generic[T]):
    
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    items: List[T] = Field(..., description="List of items")


class SuccessResponse(BaseModel, Generic[T]):
    
    success: bool = Field(True)
    message: str = Field(..., description="Response message")
    data: Optional[T] = Field(None, description="Response data")


class ErrorResponse(BaseModel):
    
    success: bool = Field(False)
    message: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    detail: Optional[str] = Field(None, description="Error details")


class MessageResponse(BaseModel):
    
    message: str = Field(..., description="Response message")
    success: bool = Field(True, description="Operation success status")


class TimestampedModel(BaseModel):
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
