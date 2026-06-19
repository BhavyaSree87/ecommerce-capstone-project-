from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class UserRegister(BaseModel):
    
    name: str = Field(..., min_length=1, max_length=100, example="Jane Doe")
    email: EmailStr = Field(..., example="jane.doe@example.com")
    password: str = Field(..., min_length=6, max_length=100, example="SecurePassword123")
    mobile: str = Field(..., pattern=r"^\d{10}$", example="9876543210")
    address: str = Field(..., min_length=5, max_length=255, example="123 Main Street")
    city: str = Field(..., min_length=1, max_length=50, example="Hyderabad")
    state: str = Field(..., min_length=1, max_length=50, example="Telangana")
    pincode: str = Field(..., pattern=r"^\d{6}$", example="500001")

    model_config = ConfigDict(str_strip_whitespace=True)


class UserLogin(BaseModel):
    
    email: EmailStr = Field(..., example="jane.doe@example.com")
    password: str = Field(..., min_length=6, example="SecurePassword123")

    model_config = ConfigDict(str_strip_whitespace=True)


class UserUpdate(BaseModel):
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    mobile: Optional[str] = Field(None, pattern=r"^\d{10}$")
    address: Optional[str] = Field(None, min_length=5, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=50)
    state: Optional[str] = Field(None, min_length=1, max_length=50)
    pincode: Optional[str] = Field(None, pattern=r"^\d{6}$")

    model_config = ConfigDict(str_strip_whitespace=True)


class UserOut(BaseModel):
    
    id: int = Field(..., description="User ID")
    name: str = Field(..., description="User name")
    email: EmailStr = Field(..., description="User email")
    role: str = Field(..., description="User role (ADMIN/CUSTOMER)")
    mobile: str = Field(..., description="User mobile")
    address: str = Field(..., description="User address")
    city: str = Field(..., description="User city")
    state: str = Field(..., description="User state")
    pincode: str = Field(..., description="User pincode")
    created_at: Optional[datetime] = Field(None, description="Account creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiry time in seconds")
    user: Optional[UserOut] = Field(None, description="Current user information")

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    
    total: int = Field(..., description="Total users count")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Items per page")
    items: List[UserOut] = Field(..., description="List of users")

    model_config = ConfigDict(from_attributes=True)

