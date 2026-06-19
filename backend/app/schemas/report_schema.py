from pydantic import BaseModel, Field, ConfigDict
from typing import List


class DashboardReport(BaseModel):
    total_users: int = Field(..., description="Total registered users")
    total_products: int = Field(..., description="Total products")
    total_orders: int = Field(..., description="Total orders")
    total_payments: int = Field(..., description="Total payment records")
    total_revenue: float = Field(..., description="Total successful revenue")
    pending_orders: int = Field(..., description="Orders currently pending")
    completed_orders: int = Field(..., description="Orders completed/delivered")

    model_config = ConfigDict(from_attributes=True)


class TopSellingProduct(BaseModel):
    product_id: int = Field(..., description="Product ID")
    product_name: str = Field(..., description="Product name")
    total_quantity_sold: int = Field(..., description="Total quantity sold")

    model_config = ConfigDict(from_attributes=True)


class MonthlyRevenueItem(BaseModel):
    month: str = Field(..., description="Revenue month in YYYY-MM format")
    revenue: float = Field(..., description="Total revenue for the month")

    model_config = ConfigDict(from_attributes=True)


class LowStockProduct(BaseModel):
    product_id: int = Field(..., description="Product ID")
    product_name: str = Field(..., description="Product name")
    stock: int = Field(..., description="Remaining stock quantity")

    model_config = ConfigDict(from_attributes=True)


class PaymentSummary(BaseModel):
    total_payments: int = Field(..., description="Total number of payments")
    successful_payments: int = Field(..., description="Successful payments count")
    pending_payments: int = Field(..., description="Pending payments count")
    failed_payments: int = Field(..., description="Failed payments count")
    total_amount: float = Field(..., description="Total payment amount")

    model_config = ConfigDict(from_attributes=True)
