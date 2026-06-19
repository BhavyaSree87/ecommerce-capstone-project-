from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from enum import Enum


class OrderStatusEnum(str, Enum):
    
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    RETURNED = "RETURNED"


class OrderItemCreate(BaseModel):
    
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, le=1000, description="Quantity")
    price: float = Field(..., gt=0, description="Unit price at time of order")

    model_config = ConfigDict()


class OrderPlace(BaseModel):
    
    items: List[OrderItemCreate] = Field(..., min_items=1, description="Order items")
    shipping_address: str = Field(..., min_length=5, max_length=500, example="123 Main Street, Hyderabad")
    billing_address: Optional[str] = Field(None, min_length=5, max_length=500)
    payment_method: str = Field(..., min_length=1, max_length=100, example="Credit Card")
    notes: Optional[str] = Field(None, max_length=500, description="Order notes")

    model_config = ConfigDict(str_strip_whitespace=True)


class OrderStatusUpdate(BaseModel):
    
    status: OrderStatusEnum = Field(..., description="New order status")
    notes: Optional[str] = Field(None, max_length=500, description="Status change notes")

    model_config = ConfigDict(str_strip_whitespace=True)


class OrderItemOut(BaseModel):
    
    order_id: int = Field(..., description="Order ID")
    item_id: int = Field(..., description="Item ID")
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., description="Quantity")
    price: float = Field(..., description="Price per unit")
    subtotal: float = Field(..., description="Line total")

    model_config = ConfigDict(from_attributes=True)


class OrderOut(BaseModel):
    
    order_id: int = Field(..., description="Order ID")
    user_id: int = Field(..., description="User ID")
    total_amount: float = Field(..., description="Total order amount")
    status: str = Field(..., description="Order status")
    shipping_address: str = Field(..., description="Shipping address")
    billing_address: Optional[str] = None
    payment_method: str = Field(..., description="Payment method used")
    items: List[OrderItemOut] = Field(..., description="Order items")
    created_at: datetime = Field(..., description="Order creation timestamp")
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class OrderDetailResponse(OrderOut):
    
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class OrderPlacedResponse(BaseModel):
    
    order_id: int = Field(..., description="Newly created order ID")
    user_id: int = Field(..., description="User ID")
    total_amount: float = Field(..., description="Total amount")
    status: str = Field(..., description="Order status")
    items: List[OrderItemOut] = Field(..., description="Items in order")
    message: str = Field("Order placed successfully", description="Status message")

    model_config = ConfigDict(from_attributes=True)


class OrderHistoryResponse(BaseModel):
    
    total: int = Field(..., description="Total orders count")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Items per page")
    items: List[OrderOut] = Field(..., description="Order list")

    model_config = ConfigDict(from_attributes=True)


class CancelOrderRequest(BaseModel):
    
    reason: Optional[str] = Field(None, max_length=500, description="Cancellation reason")

    model_config = ConfigDict(str_strip_whitespace=True)
