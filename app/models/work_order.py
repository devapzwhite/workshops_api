
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, Enum,Text,func
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.enums import StatusWorkOrder


class WorkOrder(Base):
    __tablename__ = "work_orders"
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey('workshops.id', ondelete='CASCADE'))
    vehicle_id = Column(Integer, ForeignKey('vehicles.id', ondelete='CASCADE'))
    created_by_user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    check_in_at = Column(DateTime(timezone=True),nullable=False, server_default=func.now())
    check_out_at = Column(DateTime(timezone=True),nullable=True)
    initial_diagnosis = Column(Text, nullable=True)
    labor_estimate = Column(Numeric(12,2), default=0)
    parts_estimate = Column(Numeric(precision=12,scale=2), default=0)
    status = Column(Enum(StatusWorkOrder,create_constraint=True,native_enum=False),nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True),nullable=True, server_default=func.now())
    workshop = relationship("Workshop", back_populates="work_orders")
    vehicles = relationship("Vehicle", back_populates="work_orders")
    user = relationship("User", back_populates="work_orders")
    workorder_items = relationship("WorkOrderItem", back_populates="work_order")

