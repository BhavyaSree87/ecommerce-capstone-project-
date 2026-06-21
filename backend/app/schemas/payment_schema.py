from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from enum import Enum


class PaymentMethodEnum(str, Enum):
    
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    NET_BANKING = "NET_BANKING"
    UPI = "UPI"
    WALLET = "WALLET"
    COD = "COD"
    TEST = "TEST"


class PaymentStatusEnum(str, Enum):
    
    PENDING = "PENDING"
    PAID = "PAID"
    INITIATED = "INITIATED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


class PaymentCreate(BaseModel):
    
    order_id: int = Field(..., gt=0, description="Order ID")
    payment_method: str = Field(..., description="Payment method")
    payment_status: Optional[PaymentStatusEnum] = Field(PaymentStatusEnum.PENDING, description="Payment status")
    amount: float = Field(..., gt=0, description="Payment amount")
    transaction_id: Optional[str] = Field(None, max_length=100, description="External transaction ID")
    razorpay_order_id: Optional[str] = Field(None, max_length=100, description="Razorpay order ID")
    razorpay_payment_id: Optional[str] = Field(None, max_length=100, description="Razorpay payment ID")

    model_config = ConfigDict(str_strip_whitespace=True)


class RazorpayOrderCreateRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Amount in INR")
    currency: str = Field("INR", description="Currency code")
    receipt: str = Field(..., min_length=1, description="Receipt identifier")
    notes: Optional[dict] = Field(None, description="Order notes")

    model_config = ConfigDict(str_strip_whitespace=True)


class RazorpayOrderResponse(BaseModel):
    razorpay_order_id: str = Field(..., description="Razorpay order ID")
    amount: int = Field(..., description="Amount in paise")
    currency: str = Field(..., description="Currency code")
    receipt: str = Field(..., description="Receipt ID")
    status: str = Field(..., description="Order status")

    model_config = ConfigDict(from_attributes=True)


class RazorpayVerifyRequest(BaseModel):
    razorpay_order_id: str = Field(..., description="Razorpay order ID")
    razorpay_payment_id: str = Field(..., description="Razorpay payment ID")
    razorpay_signature: str = Field(..., description="Razorpay payment signature")

    model_config = ConfigDict(str_strip_whitespace=True)


class PaymentOut(BaseModel):
   
    payment_id: int = Field(..., description="Payment ID")
    order_id: int = Field(..., description="Order ID")
    payment_method: str = Field(..., description="Payment method")
    payment_status: str = Field(..., description="Payment status")
    amount: float = Field(..., description="Payment amount")
    transaction_id: Optional[str] = None
    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedPayments(BaseModel):
    
    total: int = Field(..., description="Total payments count")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Items per page")
    items: List[PaymentOut] = Field(..., description="Payments list")

    model_config = ConfigDict(from_attributes=True)


class PaymentStatusUpdateRequest(BaseModel):
    
    status: PaymentStatusEnum = Field(..., description="New payment status")
    notes: Optional[str] = Field(None, max_length=500)

    model_config = ConfigDict(str_strip_whitespace=True)

