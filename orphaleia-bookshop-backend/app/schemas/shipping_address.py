from typing import Optional

from pydantic import BaseModel


# Shared properties
class ShippingAddressBase(BaseModel):
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None


# Properties to receive via API on creation
class ShippingAddressCreate(ShippingAddressBase):
    street_address: str
    city: str
    state: str
    postal_code: str
    country: str


# Properties to receive via API on update
class ShippingAddressUpdate(ShippingAddressBase):
    pass


# Properties shared by models stored in DB
class ShippingAddressInDBBase(ShippingAddressBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True


# Additional properties to return via API
class ShippingAddress(ShippingAddressInDBBase):
    pass


# Additional properties stored in DB
class ShippingAddressInDB(ShippingAddressInDBBase):
    pass 