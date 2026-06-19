from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class ProductBase(BaseModel):

    product_name: str = Field(..., min_length=1, max_length=255, example="Wireless Headphones")
    price: float = Field(..., gt=0, example=2499.99)
    description: str = Field(..., min_length=10, max_length=1000, example="Comfortable over-ear wireless headphones")
    category: str = Field(..., min_length=1, max_length=100, example="Electronics")
    brand: str = Field(..., min_length=1, max_length=100, example="Sony")
    stock: int = Field(..., ge=0, example=120)
    image_url: Optional[str] = Field(None, example="https://example.com/image.jpg")
    rating: Optional[float] = Field(None, ge=0, le=5, example=4.5)

    model_config = ConfigDict(str_strip_whitespace=True)


class ProductCreate(ProductBase):
    
    pass


class ProductUpdate(BaseModel):
    
    product_name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    brand: Optional[str] = Field(None, min_length=1, max_length=100)
    stock: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=5)

    model_config = ConfigDict(str_strip_whitespace=True)


class ProductOut(ProductBase):
    
    product_id: int = Field(..., description="Product ID")

    model_config = ConfigDict(from_attributes=True)


class ProductDetailResponse(ProductOut):
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedProducts(BaseModel):
    
    total: int = Field(..., description="Total products count")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Items per page")
    items: List[ProductOut] = Field(..., description="List of products")

    model_config = ConfigDict(from_attributes=True)


class ProductSearchFilters(BaseModel):
    
    keyword: Optional[str] = Field(None, max_length=100, description="Search keyword")
    category: Optional[str] = Field(None, max_length=100, description="Product category")
    brand: Optional[str] = Field(None, max_length=100, description="Product brand")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Minimum rating")
    in_stock_only: bool = Field(False, description="Only show in-stock products")

    model_config = ConfigDict(str_strip_whitespace=True)

