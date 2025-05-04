from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Shared properties
class BookBase(BaseModel):
    title: str
    author: str
    description: str
    cover: str
    price: float
    category: str
    publication_date: str
    publisher: str
    isbn: str
    pages: int
    format: str
    featured: Optional[bool] = False


# Properties to receive on book creation
class BookCreate(BookBase):
    id: Optional[str] = None
    stock: int = 0


# Properties to receive on book update
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    cover: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    publication_date: Optional[str] = None
    publisher: Optional[str] = None
    isbn: Optional[str] = None
    pages: Optional[int] = None
    format: Optional[str] = None
    featured: Optional[bool] = None
    stock: Optional[int] = None


# Properties shared by models stored in DB
class BookInDBBase(BookBase):
    id: str
    stock: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Properties to return to client
class Book(BookInDBBase):
    pass


# Properties properties stored in DB
class BookInDB(BookInDBBase):
    pass 