from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class GenerateDescriptionRequest(BaseModel):
    
    product_name: str = Field(..., min_length=1, max_length=255, example="Wireless Headphones")
    category: str = Field(..., min_length=1, max_length=100, example="Electronics")
    brand: str = Field(..., min_length=1, max_length=100, example="Sony")

    model_config = ConfigDict(str_strip_whitespace=True)


class GenerateDescriptionResponse(BaseModel):
    
    generated_description: str = Field(..., example="Premium wireless headphones with active noise cancellation, 30-hour battery life, and superior sound quality. Perfect for music lovers and professionals.")


class ShoppingAssistantRequest(BaseModel):
    
    query: str = Field(..., min_length=3, max_length=500, example="Suggest best phone under 50000")

    model_config = ConfigDict(str_strip_whitespace=True)


class ShoppingAssistantProduct(BaseModel):
    product_id: int = Field(..., example=1)
    product_name: str = Field(..., example="Dell Gaming Laptop")
    price: float = Field(..., example=89999.99)
    category: str = Field(..., example="Electronics")
    brand: str = Field(..., example="Dell")
    stock: int = Field(..., example=15)
    rating: Optional[float] = Field(None, example=4.5)
    image_url: Optional[str] = Field(None, example="https://example.com/image.jpg")


class ShoppingAssistantResponse(BaseModel):
    success: bool = Field(..., example=True)
    message: str = Field(..., example="Found 5 matching products")
    answer: Optional[str] = Field(None, example="Based on your query, here are the best matches...")
    products: List[ShoppingAssistantProduct] = Field(default_factory=list)


class ProductSearchRequest(BaseModel):
    
    query: str = Field(..., min_length=2, max_length=100, example="gaming laptop")

    model_config = ConfigDict(str_strip_whitespace=True)


class ProductSearchResult(BaseModel):
    
    product_id: int = Field(..., example=1)
    product_name: str = Field(..., example="Dell Gaming Laptop")
    price: float = Field(..., example=89999.99)
    category: str = Field(..., example="Electronics")
    brand: str = Field(..., example="Dell")
    stock: int = Field(..., example=15)
    rating: Optional[float] = Field(None, example=4.5)
    image_url: Optional[str] = Field(None, example="https://example.com/image.jpg")
    relevance_score: float = Field(..., example=95.5, description="Relevance score 0-100")


class ProductSearchResponse(BaseModel):
    
    query: str = Field(..., example="gaming laptop")
    total_results: int = Field(..., example=5)
    results: List[ProductSearchResult] = Field(..., example=[])


