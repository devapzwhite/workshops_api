from typing import Annotated,List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from app.core.security import current_user as get_current_user
from app.dependencies import get_db
from app.models.user import User
from app.schemas.vehicle import VehicleRead, CreateVehicle, VehicleUpdate
from app.services.vehicle_service import get_vehicles_by_workshop, get_vehicle_by_plate, new_vehicle, modify_vehicle

router = APIRouter(prefix="/vehicles",tags=["vehicles"])

@router.get("", response_model=List[VehicleRead])
async def get_vehicles(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User,Depends( get_current_user)],):
    return await get_vehicles_by_workshop(db=db,workshop_id=current_user.shop_id)


@router.get("/{plate}", response_model=VehicleRead)
async def search_vehicle_by_plate(
        plate: str,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[User,Depends(get_current_user)]):
    return await get_vehicle_by_plate(plate=plate,db=db,workshop_id=current_user.shop_id)


@router.post("", response_model=VehicleRead)
async def create_vehicle(
        vehicle: CreateVehicle,
        db: Annotated[AsyncSession,Depends(get_db)],
        current_user: Annotated[User,Depends(get_current_user)]):
    workshop_id = current_user.shop_id
    return await new_vehicle(db=db,vehicle=vehicle,workshop_id=workshop_id)


@router.put("/{id}", response_model=VehicleRead)
async def update_vehicle(
        id: int,
        payload: VehicleUpdate,
        db: Annotated[AsyncSession,Depends(get_db)],
        current_user: Annotated[User,Depends(get_current_user)]):
    return await modify_vehicle(id=id,payload=payload,db=db,shop_id= current_user.shop_id)
