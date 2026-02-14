from sqlalchemy import Integer, Column, ForeignKey, String, Text, DateTime, Enum, func, UniqueConstraint

from sqlalchemy.orm import relationship

from app.db.database import Base
from app.enums import TipoVehiculo


class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey('workshops.id'),nullable=False,index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"))
    vehicle_type = Column(Enum(TipoVehiculo,create_constraint=True,native_enum=False), nullable=False)
    plate = Column(String(20), nullable=False)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=True)
    photo_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    workshop = relationship("Workshop", back_populates="vehicles")
    customer = relationship("Customer", back_populates='vehicles')
    work_orders = relationship("WorkOrder", back_populates='vehicles')

    __table_args__ = (
        UniqueConstraint("shop_id", "plate", name="uq_shop_plate"),
    )
