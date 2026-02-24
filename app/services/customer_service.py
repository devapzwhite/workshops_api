from http.client import responses

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException,status
from app.models.user import User
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerRead


async def get_customer_by_workshop(document_id: str, db: AsyncSession, user: User):
    response = await db.execute(select(Customer).where(Customer.shop_id == user.shop_id,Customer.document_id == document_id))
    customer = response.scalars().first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customer not found")
    return customer

async def add_customer(data: CustomerCreate, db: AsyncSession, user: User):
    if await _exists_customer_by_rut(customer_rut=data.document_id,customer_shop_id=user.shop_id, db=db):
        raise HTTPException(status_code=400,detail="Customer with that document_id already exists")
    customer = Customer(
        document_id=data.document_id,
        name=data.name,
        last_name=data.last_name,
        phone=data.phone,
        email=data.email,
        address=data.address,
        shop_id=user.shop_id
    )
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer



async def _exists_customer_by_rut(customer_rut: str,customer_shop_id: int, db: AsyncSession) -> bool:
    response = await db.execute(select(Customer).where(Customer.shop_id == customer_shop_id,Customer.document_id == customer_rut))
    exists = response.scalars().first()
    if exists:
        return True
    return False

async def update_customer_by_id(customer_id: int, payload: CustomerUpdate,db: AsyncSession, current_user: User):
    customer = await get_customer_by_id(id= customer_id, db=db,workshop=current_user.shop_id)
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)
    await db.commit()
    await db.refresh(customer)
    return customer



async def get_customer_by_id(id: int,db: AsyncSession, workshop: int):
    response = await db.execute(select(Customer).where(Customer.shop_id == workshop,Customer.id == id))
    get_customer = response.scalars().first()
    if not get_customer:
        raise HTTPException(status_code=404,detail="Customer not found in the workshop")
    return get_customer