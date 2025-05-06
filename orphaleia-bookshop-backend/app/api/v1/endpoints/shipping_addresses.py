from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app import models, schemas
from app.api import deps

router = APIRouter()


@router.get("/me", response_model=schemas.ShippingAddress)
def read_shipping_address_me(
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get current user's shipping address.
    """
    if not current_user.shipping_address:
        raise HTTPException(
            status_code=404,
            detail="Shipping address not found",
        )
    return current_user.shipping_address


@router.post("/me", response_model=schemas.ShippingAddress)
def create_shipping_address_me(
    *,
    db: Session = Depends(deps.get_db),
    shipping_address_in: schemas.ShippingAddressCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new shipping address for current user.
    """
    # Check if user already has a shipping address
    if current_user.shipping_address:
        raise HTTPException(
            status_code=400,
            detail="User already has a shipping address. Use PUT to update.",
        )
    
    # Create new shipping address
    address_id = str(uuid.uuid4())
    shipping_address = models.ShippingAddress(
        id=address_id,
        user_id=current_user.id,
        street_address=shipping_address_in.street_address,
        city=shipping_address_in.city,
        state=shipping_address_in.state,
        postal_code=shipping_address_in.postal_code,
        country=shipping_address_in.country,
    )
    db.add(shipping_address)
    db.commit()
    db.refresh(shipping_address)
    return shipping_address


@router.put("/me", response_model=schemas.ShippingAddress)
def update_shipping_address_me(
    *,
    db: Session = Depends(deps.get_db),
    shipping_address_in: schemas.ShippingAddressUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update current user's shipping address.
    """
    if not current_user.shipping_address:
        # If user doesn't have an address yet, create one
        address_id = str(uuid.uuid4())
        shipping_address = models.ShippingAddress(
            id=address_id,
            user_id=current_user.id,
        )
        db.add(shipping_address)
    else:
        shipping_address = current_user.shipping_address
    
    update_data = shipping_address_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(shipping_address, field, value)
    
    db.add(shipping_address)
    db.commit()
    db.refresh(shipping_address)
    return shipping_address


@router.delete("/me", response_model=schemas.ShippingAddress)
def delete_shipping_address_me(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete current user's shipping address.
    """
    if not current_user.shipping_address:
        raise HTTPException(
            status_code=404,
            detail="Shipping address not found",
        )
    
    shipping_address = current_user.shipping_address
    db.delete(shipping_address)
    db.commit()
    return shipping_address 