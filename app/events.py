from sqlalchemy import event, select, func
from app.models.work_order_item import WorkOrderItem
from app.models.work_order import WorkOrder

def recalculate_labor_estimate(mapper, connection, target):
    # target = el WorkOrderItem que se insertó/modificó/eliminó
    connection.execute(
        WorkOrder.__table__
        .update()
        .where(WorkOrder.__table__.c.id == target.work_order_id)
        .values(
            labor_estimate=(
                select(func.coalesce(func.sum(
                    WorkOrderItem.__table__.c.unit_price *
                    WorkOrderItem.__table__.c.quantity
                ), 0))
                .where(WorkOrderItem.__table__.c.work_order_id == target.work_order_id)
                .scalar_subquery()
            )
        )
    )

event.listens_for(WorkOrderItem, "after_insert")(recalculate_labor_estimate)
event.listens_for(WorkOrderItem, "after_update")(recalculate_labor_estimate)
event.listens_for(WorkOrderItem, "after_delete")(recalculate_labor_estimate)
