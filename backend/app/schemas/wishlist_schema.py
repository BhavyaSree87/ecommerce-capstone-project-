from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class WishlistCreate(BaseModel):
    
    product_id: int = Field(..., gt=0, description="Product ID to add")

    model_config = ConfigDict()


class WishlistItemOut(BaseModel):
    
    wishlist_id: int = Field(..., description="Wishlist item ID")
    user_id: int = Field(..., description="User ID")
    product_id: int = Field(..., description="Product ID")
    product_name: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class WishlistResponse(BaseModel):
    
    total_items: int = Field(..., description="Total items in wishlist")
    items: List[WishlistItemOut] = Field(..., description="Wishlist items")

    model_config = ConfigDict(from_attributes=True)
