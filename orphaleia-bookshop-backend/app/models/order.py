from datetime import datetime
from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Order(Base):
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    status = Column(
        Enum("pending", "processing", "shipped", "delivered", "cancelled", name="order_status"),
        default="pending"
    )
    total_amount = Column(Float, nullable=False)
    shipping_address = Column(Text, nullable=False)
    payment_id = Column(String, nullable=True)  # External payment reference
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    id = Column(String, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("order.id"), nullable=False)
    book_id = Column(String, ForeignKey("book.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)  # Stored at time of purchase
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    book = relationship("Book", back_populates="order_items") 