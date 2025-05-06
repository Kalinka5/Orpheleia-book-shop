from datetime import datetime
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, Field


# Define the allowed order status values
class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# OrderItem schemas
class OrderItemBase(BaseModel):
    book_id: str
    quantity: int
    unit_price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None


class OrderItemInDBBase(OrderItemBase):
    id: str
    order_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class OrderItem(OrderItemInDBBase):
    pass


# Order schemas
class OrderBase(BaseModel):
    shipping_address: str


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    shipping_address: Optional[str] = None
    payment_id: Optional[str] = None


class OrderInDBBase(OrderBase):
    id: str
    user_id: str
    status: str
    total_amount: float
    payment_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    item_count: Optional[int] = None

    class Config:
        from_attributes = True


class Order(OrderInDBBase):
    items: List[OrderItem]


class OrderInDB(OrderInDBBase):
    pass 