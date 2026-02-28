from fastapi import APIRouter

from app.schemas.work_order_item import WorkOrderItemResponse

router = APIRouter('/workorderitem', tags=['Work Order Item'])



@router.get('/',response_model=WorkOrderItemResponse)
async def get_workorder_item():
    pass

@router.post('/',response_model=WorkOrderItemResponse)
async def create_workorder_item():
    pass

@router.put('/{id}',response_model=WorkOrderItemResponse)
async def update_workorder_item():
    pass

@router.delete('/{id}',response_model=WorkOrderItemResponse)
async def delete_workorder_item():
    pass
