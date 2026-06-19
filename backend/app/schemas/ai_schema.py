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


class ShoppingAssistantResponse(BaseModel):
    
    answer: str = Field(..., example="Based on your budget of 50000, I recommend the Samsung Galaxy A50 at 45,999 with excellent camera quality and battery life. Another great option is the Redmi Note 9 Pro at 42,999 with a high refresh rate display.")


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
    relevance_score: float = Field(..., example=95.5, description="Relevance score 0-100")


class ProductSearchResponse(BaseModel):
    
    query: str = Field(..., example="gaming laptop")
    total_results: int = Field(..., example=5)
    results: List[ProductSearchResult] = Field(..., example=[])


