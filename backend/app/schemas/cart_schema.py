from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class CartCreate(BaseModel):
    
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, le=1000, description="Quantity")

    model_config = ConfigDict()


class CartUpdate(BaseModel):
    
    quantity: int = Field(..., gt=0, le=1000, description="New quantity")

    model_config = ConfigDict()


class CartItemOut(BaseModel):
    
    cart_id: int = Field(..., description="Cart item ID")
    user_id: int = Field(..., description="User ID")
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., description="Quantity")
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CartResponse(BaseModel):
    
    total_items: int = Field(..., description="Total items in cart")
    items: List[CartItemOut] = Field(..., description="Cart items")

    model_config = ConfigDict(from_attributes=True)
