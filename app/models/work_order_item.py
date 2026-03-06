from sqlalchemy import DateTime, func, Integer, Column, ForeignKey, Enum, TEXT, NUMERIC
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.enums import WorkOrderItemType


class WorkOrderItem(Base):
    __tablename__ = 'work_order_items'
    id = Column(Integer, primary_key=True, nullable=False,index=True)
    work_order_id = Column(Integer, ForeignKey('work_orders.id',ondelete='CASCADE'),nullable=False, index=True)
    item_type = Column(Enum(WorkOrderItemType,values_callable=lambda e: [i.value for i in e], create_constraint=True,native_enum=False), nullable=False)
    description = Column(TEXT, nullable=False)
    quantity = Column(Integer,default=1, nullable=False)
    unit_cost = Column(NUMERIC(12,2),default=0, server_default="0", nullable=False)
    unit_price = Column(NUMERIC(12,2),default=0, server_default="0", nullable=False)
    before_photo_url = Column(TEXT, nullable=True)
    after_photo_url = Column(TEXT, nullable=True)
    created_at = Column(DateTime(timezone=True),nullable=True, server_default=func.now())
    work_order = relationship("WorkOrder", back_populates="workorder_items")