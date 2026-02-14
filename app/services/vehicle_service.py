from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Workshop, Vehicle, Customer
from app.schemas.vehicle import CreateVehicle, VehicleUpdate
from psycopg2.errors import ForeignKeyViolation


def get_vehicles_by_workshop(
        workshop_id: int,
        db: Session
)->List[Vehicle]:
    workshop = db.query(Workshop).filter(Workshop.id == workshop_id).first()
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    return workshop.vehicles

def get_vehicle_by_plate(
        plate: str,
        db: Session,
        workshop_id: int
)-> type[Vehicle]:
    vehicle = db.query(Vehicle).filter(Vehicle.shop_id == workshop_id,
                                       Vehicle.plate == plate).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

def new_vehicle(vehicle: CreateVehicle, db: Session ,workshop_id: int)-> Vehicle:
    if _exists_vehicle(db=db,vehicle_workshop_id=workshop_id,vehicle_plate=vehicle.plate):
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
    db.commit()
    db.refresh(vehicle_to_create)
    return vehicle_to_create

def modify_vehicle(id: int,db:Session,payload:VehicleUpdate, shop_id: int)-> Vehicle:
    vehicle: Vehicle | None= db.query(Vehicle).filter(Vehicle.id == id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "customer_id" in update_data:
        if not _exists_customer_by_id(db=db, id=update_data["customer_id"],shop_id=shop_id):
            raise HTTPException(status_code=404, detail="Customer not found")
    if "plate" in update_data:
        if _exists_vehicle(vehicle_plate=update_data["plate"], db=db, vehicle_workshop_id=shop_id):
            raise HTTPException(status_code=400, detail="Plate already exists")
    print(update_data["plate"])
    for key, value in update_data.items():
        setattr(vehicle, key, value)

    db.commit()
    db.refresh(vehicle)
    return vehicle

def _exists_customer_by_id(db: Session, id: int,shop_id: int)->bool:
    customer = db.query(Customer).filter(Customer.shop_id == shop_id ,Customer.id == id).first()
    if not customer:
        return False
    return True


def _exists_vehicle(vehicle_plate: str, vehicle_workshop_id: int, db: Session) -> bool:
        exists = db.query(Vehicle).filter(Vehicle.shop_id == vehicle_workshop_id,
                                          Vehicle.plate == vehicle_plate).first()
        if exists:
            return True
        else:
            return False
