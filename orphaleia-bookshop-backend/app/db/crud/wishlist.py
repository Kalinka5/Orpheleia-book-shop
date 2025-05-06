import uuid
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.wishlist import WishlistItem
from app.schemas.wishlist import WishlistItemCreate


def get_wishlist_items(db: Session, user_id: str) -> List[WishlistItem]:
    """Get all wishlist items for a user, with book details loaded"""
    return db.query(WishlistItem).filter(WishlistItem.user_id == user_id).all()


def get_wishlist_item(db: Session, user_id: str, book_id: str) -> Optional[WishlistItem]:
    """Get a specific wishlist item by user_id and book_id"""
    return db.query(WishlistItem).filter(
        WishlistItem.user_id == user_id,
        WishlistItem.book_id == book_id
    ).first()


def create_wishlist_item(db: Session, user_id: str, item_in: WishlistItemCreate) -> WishlistItem:
    """Add a book to the user's wishlist"""
    # Check if the item is already in the wishlist
    existing_item = get_wishlist_item(db, user_id, item_in.book_id)
    if existing_item:
        return existing_item
    
    # Create new wishlist item
    db_item = WishlistItem(
        id=str(uuid.uuid4()),
        user_id=user_id,
        book_id=item_in.book_id
    )
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Book or user does not exist, or item is already in wishlist"
        )


def delete_wishlist_item(db: Session, user_id: str, book_id: str) -> bool:
    """Remove a book from the user's wishlist"""
    item = get_wishlist_item(db, user_id, book_id)
    if not item:
        return False
    
    db.delete(item)
    db.commit()
    return True


def check_wishlist_item_exists(db: Session, user_id: str, book_id: str) -> bool:
    """Check if a book is in the user's wishlist"""
    return db.query(WishlistItem).filter(
        WishlistItem.user_id == user_id,
        WishlistItem.book_id == book_id
    ).count() > 0 