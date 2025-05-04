from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.core.security import generate_uuid

router = APIRouter()


@router.post("/", response_model=schemas.Order)
def create_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: schemas.OrderCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new order.
    """
    # Calculate total amount based on cart items
    total_amount = 0
    order_items = []
    
    for item in order_in.items:
        book = db.query(models.Book).filter(models.Book.id == item.book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail=f"Book with ID {item.book_id} not found")
        
        # Check if book is in stock
        if book.stock < item.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Not enough stock for book '{book.title}'. Available: {book.stock}"
            )
        
        total_amount += book.price * item.quantity
        
        # Create order item
        order_items.append({
            "book_id": item.book_id,
            "quantity": item.quantity,
            "unit_price": book.price
        })
        
        # Update book stock
        book.stock -= item.quantity
        db.add(book)
    
    # Create order
    order_id = generate_uuid()
    order = models.Order(
        id=order_id,
        user_id=current_user.id,
        total_amount=total_amount,
        shipping_address=order_in.shipping_address,
        status="pending"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Add order items
    for item_data in order_items:
        item = models.OrderItem(
            id=generate_uuid(),
            order_id=order.id,
            **item_data
        )
        db.add(item)
    
    db.commit()
    db.refresh(order)
    
    return order


@router.get("/", response_model=List[schemas.Order])
def read_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve orders.
    """
    if current_user.is_admin:
        # Admin can see all orders
        orders = db.query(models.Order).offset(skip).limit(limit).all()
    else:
        # Regular users can only see their own orders
        orders = db.query(models.Order).filter(
            models.Order.user_id == current_user.id
        ).offset(skip).limit(limit).all()
    
    return orders


@router.get("/user", response_model=List[schemas.Order])
def read_user_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve current user's orders.
    """
    orders = db.query(models.Order).filter(
        models.Order.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return orders


@router.get("/{order_id}", response_model=schemas.Order)
def read_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get order by ID.
    """
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check permission
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return order


@router.put("/{order_id}", response_model=schemas.Order)
def update_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: str,
    order_in: schemas.OrderUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an order.
    
    Valid status values are: "pending", "processing", "shipped", "delivered", "cancelled"
    """
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check permission (only admin can update order status)
    if not current_user.is_admin and order_in.status:
        raise HTTPException(status_code=403, detail="Not enough permissions to update status")
    
    # Users can only update their own shipping address
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = order_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    
    db.add(order)
    db.commit()
    db.refresh(order)
    return order 