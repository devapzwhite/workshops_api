from fastapi import APIRouter

router = APIRouter(prefix="/vehicles",tags=["vehicles"])

@router.get("/")
async def root_vehicles():
    return {"message": "Hello World from vehicles"}