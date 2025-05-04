from fastapi import APIRouter

from app.api.v1.endpoints import auth, books, orders, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"]) 