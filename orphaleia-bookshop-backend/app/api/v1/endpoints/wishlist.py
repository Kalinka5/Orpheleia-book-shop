from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.db.crud import wishlist as crud_wishlist
from app.models.user import User
from app.models.book import Book
from app.schemas.wishlist import WishlistItemCreate, WishlistItemWithBook

router = APIRouter()


@router.get("/", response_model=List[WishlistItemWithBook])
def get_wishlist(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get the current user's wishlist
    """
    items = crud_wishlist.get_wishlist_items(db, current_user.id)
    # Convert DB model items to schema with loaded books
    result = []
    for item in items:
        # Explicitly load the book for each wishlist item
        book = db.query(Book).filter(Book.id == item.book_id).first()
        wishlist_item_with_book = WishlistItemWithBook(
            id=item.id,
            user_id=item.user_id,
            book_id=item.book_id,
            added_at=item.added_at,
            book=book
        )
        result.append(wishlist_item_with_book)
    return result


@router.post("/", response_model=WishlistItemWithBook, status_code=status.HTTP_201_CREATED)
def add_to_wishlist(
    item_in: WishlistItemCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Add a book to the current user's wishlist
    """
    # Check if the book exists
    book = db.query(Book).filter(Book.id == item_in.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Add to wishlist
    item = crud_wishlist.create_wishlist_item(db, current_user.id, item_in)
    
    # Return with book details
    return WishlistItemWithBook(
        id=item.id,
        user_id=item.user_id,
        book_id=item.book_id,
        added_at=item.added_at,
        book=book
    )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_wishlist(
    book_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Remove a book from the current user's wishlist
    """
    result = crud_wishlist.delete_wishlist_item(db, current_user.id, book_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found in wishlist"
        )
    return None


@router.get("/check/{book_id}", response_model=dict)
def check_wishlist_item(
    book_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Check if a book is in the current user's wishlist
    """
    exists = crud_wishlist.check_wishlist_item_exists(db, current_user.id, book_id)
    return {"exists": exists} 