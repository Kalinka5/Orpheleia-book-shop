from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.core.security import generate_uuid

router = APIRouter()


@router.get("/", response_model=List[schemas.Book])
def read_books(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    featured: Optional[bool] = None,
) -> Any:
    """
    Retrieve books with optional filtering.
    """
    query = db.query(models.Book)
    
    # Filter by category
    if category and category != "all":
        query = query.filter(models.Book.category == category)
    
    # Filter by search query
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Book.title.ilike(search_term),
                models.Book.author.ilike(search_term),
                models.Book.description.ilike(search_term),
            )
        )
    
    # Filter by featured
    if featured is not None:
        query = query.filter(models.Book.featured == featured)
    
    # Apply sorting
    if sort:
        if sort == "title-asc":
            query = query.order_by(models.Book.title.asc())
        elif sort == "title-desc":
            query = query.order_by(models.Book.title.desc())
        elif sort == "price-asc":
            query = query.order_by(models.Book.price.asc())
        elif sort == "price-desc":
            query = query.order_by(models.Book.price.desc())
    else:
        # Default sorting
        query = query.order_by(models.Book.title.asc())
    
    books = query.offset(skip).limit(limit).all()
    return books


@router.post("/", response_model=schemas.Book)
def create_book(
    *,
    db: Session = Depends(deps.get_db),
    book_in: schemas.BookCreate,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Create new book (admin only).
    """
    book_id = book_in.id if book_in.id else generate_uuid()
    book = models.Book(id=book_id, **book_in.dict(exclude={"id"}))
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.get("/featured", response_model=List[schemas.Book])
def read_featured_books(
    db: Session = Depends(deps.get_db),
    limit: int = 8,
) -> Any:
    """
    Get featured books.
    """
    books = db.query(models.Book).filter(models.Book.featured == True).limit(limit).all()
    return books


@router.get("/category/{category}", response_model=List[schemas.Book])
def read_books_by_category(
    category: str,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get books by category.
    """
    books = db.query(models.Book).filter(models.Book.category == category).offset(skip).limit(limit).all()
    return books


@router.get("/{book_id}", response_model=schemas.Book)
def read_book(
    *,
    db: Session = Depends(deps.get_db),
    book_id: str,
) -> Any:
    """
    Get book by ID.
    """
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=schemas.Book)
def update_book(
    *,
    db: Session = Depends(deps.get_db),
    book_id: str,
    book_in: schemas.BookUpdate,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Update a book (admin only).
    """
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    update_data = book_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)
    
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", response_model=schemas.Book)
def delete_book(
    *,
    db: Session = Depends(deps.get_db),
    book_id: str,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Delete a book (admin only).
    """
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return book