from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class InventoryBase(BaseModel):
    
    product_id: int = Field(..., gt=0, description="Product ID", example=101)
    available_stock: int = Field(..., ge=0, description="Available stock quantity", example=50)
    reserved_stock: int = Field(0, ge=0, description="Reserved stock quantity", example=5)

    model_config = ConfigDict(str_strip_whitespace=True)


class InventoryCreate(InventoryBase):
    
    pass


class InventoryUpdate(BaseModel):
    
    available_stock: Optional[int] = Field(None, ge=0, description="Updated available stock level", example=48)
    reserved_stock: Optional[int] = Field(None, ge=0, description="Updated reserved stock level", example=7)

    model_config = ConfigDict(str_strip_whitespace=True)


class InventoryOut(InventoryBase):
    
    inventory_id: int = Field(..., description="Inventory record ID", example=1001)
    last_updated: Optional[datetime] = Field(None, description="Last inventory update timestamp")

    model_config = ConfigDict(from_attributes=True)


class PaginatedInventory(BaseModel):
    
    total: int = Field(..., description="Total inventory records")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    items: List[InventoryOut] = Field(..., description="Inventory records")

    model_config = ConfigDict(from_attributes=True)
