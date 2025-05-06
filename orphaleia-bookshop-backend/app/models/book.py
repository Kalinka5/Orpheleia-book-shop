from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Book(Base):
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    cover = Column(String, nullable=False)  # URL to image
    price = Column(Float, nullable=False)
    category = Column(String, index=True, nullable=False)
    publication_date = Column(String, nullable=False)  # Store as ISO date string
    publisher = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    pages = Column(Integer, nullable=False)
    format = Column(String, nullable=False)  # Paperback, Hardcover, etc.
    featured = Column(Boolean, default=False)
    stock = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="book")
    # wishlisted_by relationship is defined in WishlistItem model with backref 