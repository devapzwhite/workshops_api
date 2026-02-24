from http.client import responses
from typing import List


from fastapi import HTTPException
from sqlalchemy.util import await_only

from app.models import Workshop, Vehicle, Customer
from app.schemas.vehicle import CreateVehicle, VehicleUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_vehicles_by_workshop(
        workshop_id: int,
        db: AsyncSession
)->List[Vehicle]:
    result = await db.execute(
        select(Vehicle)
        .where(Vehicle.shop_id == workshop_id)
    )
    vehicles = result.scalars().all()
    return list(vehicles)

async def get_vehicle_by_plate(
        plate: str,
        db: AsyncSession,
        workshop_id: int
)-> type[Vehicle]:
    result = await db.execute(select(Vehicle).where(Vehicle.shop_id == workshop_id, Vehicle.plate == plate))
    vehicle = result.scalars().first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

async def new_vehicle(vehicle: CreateVehicle, db: AsyncSession ,workshop_id: int)-> Vehicle:
    if await _exists_vehicle(db=db,vehicle_workshop_id=workshop_id,vehicle_plate=vehicle.plate):
        raise HTTPException(status_code=400, detail="Vehicle already exists")
    vehicle_to_create = Vehicle(
        shop_id=workshop_id,
        customer_id=vehicle.customer_id,
        vehicle_type=vehicle.vehicle_type,
        plate=vehicle.plate,
        brand=vehicle.brand,
        model=vehicle.model,
        year=vehicle.year,
        photo_url=vehicle.photo_url
    )
    db.add(vehicle_to_create)
    await db.commit()
    await db.refresh(vehicle_to_create)
    return vehicle_to_create

async def modify_vehicle(id: int,db:AsyncSession,payload:VehicleUpdate, shop_id: int)-> Vehicle:
    exists_vehicle = await db.execute(select(Vehicle).where(Vehicle.id == id))
    vehicle: Vehicle | None= exists_vehicle.scalars().first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "customer_id" in update_data:
        if not await _exists_customer_by_id(db=db, id=update_data["customer_id"],shop_id=shop_id):
            raise HTTPException(status_code=404, detail="Customer not found")
    if "plate" in update_data:
        if await _exists_vehicle(vehicle_plate=update_data["plate"], db=db, vehicle_workshop_id=shop_id):
            raise HTTPException(status_code=400, detail="Plate already exists")
    for key, value in update_data.items():
        setattr(vehicle, key, value)

    await db.commit()
    await db.refresh(vehicle)
    return vehicle

async def _exists_customer_by_id(db: AsyncSession, id: int,shop_id: int)->bool:
    response = await db.execute(select(Customer).where(Customer.id == id))
    customer = response.scalars().first()
    if not customer:
        return False
    return True


async def _exists_vehicle(vehicle_plate: str, vehicle_workshop_id: int, db: AsyncSession) -> bool:
        result = await db.execute(select(Vehicle).where(Vehicle.shop_id == vehicle_workshop_id, Vehicle.plate == vehicle_plate))
        exists = result.scalars().first()
        if exists:
            return True
        else:
            return False
