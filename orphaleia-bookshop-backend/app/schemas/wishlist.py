from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.book import Book


# Base schema for wishlist item shared properties
class WishlistItemBase(BaseModel):
    book_id: str


# Schema for creating a new wishlist item
class WishlistItemCreate(WishlistItemBase):
    pass


# Schema for update operations
class WishlistItemUpdate(WishlistItemBase):
    pass


# Schema for database object
class WishlistItem(WishlistItemBase):
    id: str
    user_id: str
    added_at: datetime
    
    class Config:
        from_attributes = True


# Schema for returning wishlist items with full book details
class WishlistItemWithBook(WishlistItem):
    book: Optional[Book] = None 