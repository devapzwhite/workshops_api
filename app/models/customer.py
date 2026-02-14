from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key= True, index=True)
    shop_id = Column(Integer, ForeignKey('workshops.id'),nullable=False,index=True)
    document_id = Column(String(28),nullable=False)
    name = Column(String(50),nullable=False)
    last_name = Column(String(50),nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(String(200))
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    workshop = relationship('Workshop', back_populates="customers")
    vehicles = relationship('Vehicle', back_populates="customer")
    __table_args__ = (
        UniqueConstraint('shop_id', 'document_id', name='uq_customers_shop_document'),)

