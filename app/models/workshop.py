from sqlalchemy import Column, Integer, String,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Workshop(Base):
    __tablename__ = "workshops"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False,)
    owner_name = Column(String(100))
    phone = Column(String(20))
    address = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    users = relationship("User", back_populates="workshop")
    customers = relationship("Customer", back_populates="workshop")
    vehicles = relationship("Vehicle", back_populates="workshop")
    work_orders = relationship("WorkOrder", back_populates="workshop")
