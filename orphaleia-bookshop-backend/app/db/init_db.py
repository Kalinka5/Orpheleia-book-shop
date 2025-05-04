import logging
from sqlalchemy.orm import Session

from app import models, schemas
from app.core.config import settings
from app.core.security import get_password_hash, generate_uuid
from app.db import base  # noqa: F401

from app.data.sample_books import books as sample_books

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """
    Initialize the database with seed data.
    """
    # Create admin user if it doesn't exist
    user = db.query(models.User).filter(models.User.email == "admin@orphaleia.com").first()
    if not user:
        user_id = generate_uuid()
        user_in = schemas.UserCreate(
            email="admin@orphaleia.com",
            password="adminpassword",  # This would be a more secure password in production
            full_name="Admin User",
            is_admin=True,
        )
        user = models.User(
            id=user_id,
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            is_admin=user_in.is_admin,
        )
        db.add(user)
        db.commit()
        logger.info("Admin user created")
    
    # Create sample books
    for book_data in sample_books:
        book = db.query(models.Book).filter(models.Book.isbn == book_data["isbn"]).first()
        if not book:
            book_id = book_data.get("id", generate_uuid())
            book = models.Book(
                id=book_id,
                title=book_data["title"],
                author=book_data["author"],
                description=book_data["description"],
                cover=book_data["cover"],
                price=book_data["price"],
                category=book_data["category"],
                publication_date=book_data["publicationDate"],
                publisher=book_data["publisher"],
                isbn=book_data["isbn"],
                pages=book_data["pages"],
                format=book_data["format"],
                featured=book_data.get("featured", False),
                stock=20,  # Default stock
            )
            db.add(book)
        
    db.commit()
    logger.info("Sample books created") 