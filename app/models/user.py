from sqlalchemy import Column, Integer, ForeignKey,String,Boolean,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer,ForeignKey('workshops.id', ondelete="CASCADE"), nullable=False, index=True)
    username = Column(String(50), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, server_default="true")
    created_at = Column(DateTime, server_default=func.now())
    work_orders = relationship("WorkOrder", back_populates="user")
    workshop = relationship("Workshop", back_populates="users")
    # roles = relationship("role",secondary="user_roles", back_populates="users")
