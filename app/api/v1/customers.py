from http.client import responses
from typing import List, Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.util import await_only

from app.dependencies import get_db
from app.models.user import User
from app.schemas.customer import CustomerRead, CustomerCreate, CustomerUpdate, CustomerReadDetail
from app.models.customer import Customer
from app.core.security import current_user_is_active
from app.services.customer_service import get_customer_by_workshop, add_customer, update_customer_by_id, get_customer_by_id

router = APIRouter(prefix="/customers",tags=["customers"])


@router.post("", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
async def create_customer(data: CustomerCreate, db:Annotated[AsyncSession,Depends(get_db)],user: Annotated[User,Depends(current_user_is_active)]):
    return await add_customer(data=data,db=db,user=user)


@router.get("", response_model=List[CustomerRead])
async def list_customers(db: Annotated[AsyncSession,Depends(get_db)], user: Annotated[User, Depends(current_user_is_active)]):
    response = await db.execute(select(Customer).where(Customer.shop_id == user.shop_id).order_by(Customer.id))
    customers = response.scalars().all()
    return customers


@router.get("/by_document/{document_id}", response_model=CustomerRead)
async def get_customer_by_document(document_id: str, db: Annotated[AsyncSession,Depends(get_db)], user: Annotated[User, Depends(current_user_is_active)]):
    return await get_customer_by_workshop(document_id=document_id,db=db,user=user)

@router.get('/by_id/{customer_id}', response_model=CustomerRead)
async def get_customer_id(
        customer_id: int,
        db: Annotated[AsyncSession,Depends(get_db)], user: Annotated[User,Depends(current_user_is_active)],
):
    return await get_customer_by_id(id=customer_id,db=db,workshop=user.shop_id)

@router.get('/{customer_id}/details', response_model=CustomerReadDetail)
async def get_customer_detail(
        customer_id: int,
        db: Annotated[AsyncSession,Depends(get_db)],
        user: Annotated[User,Depends(current_user_is_active)],
):
    response = await db.execute(select(Customer).where(Customer.id == customer_id).options(selectinload(Customer.workshop),selectinload(Customer.vehicles)))
    result = response.scalars().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customer not found")
    return  result


@router.put("/{customer_id}", response_model=CustomerRead)
async def update_customer(customer_id: int,payload: CustomerUpdate,db: Annotated[AsyncSession,Depends(get_db)],user: Annotated[User, Depends(current_user_is_active)]):
    return await update_customer_by_id(customer_id=customer_id,db=db,payload=payload,current_user=user)

