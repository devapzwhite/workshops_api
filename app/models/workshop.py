from sqlalchemy import Column, Integer, String,DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class Workshop(Base):
    __tablename__ = "workshops"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    owner_name = Column(String(100))
    phone = Column(String(20))
    address = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
