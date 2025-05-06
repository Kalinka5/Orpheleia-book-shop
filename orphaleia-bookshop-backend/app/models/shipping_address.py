from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ShippingAddress(Base):
    __tablename__ = "shipping_address"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    street_address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country = Column(String, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="shipping_address") 