from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class WishlistItem(Base):
    """Model for wishlist items - represents many-to-many relationship between users and books"""
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False)
    book_id = Column(String, ForeignKey("book.id", ondelete="CASCADE"), index=True, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="wishlist_items")
    book = relationship("Book", backref="wishlisted_by")
    
    # Create a composite unique constraint to prevent duplicate wishlist entries
    __table_args__ = (
        UniqueConstraint('user_id', 'book_id', name='uq_user_book_wishlist'),
    ) 