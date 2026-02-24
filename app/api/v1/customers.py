from typing import List, Annotated
from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.user import User
from app.schemas.customer import CustomerRead, CustomerCreate, CustomerUpdate, CustomerReadDetail
from app.models.customer import Customer
from app.core.security import current_user_is_active
from app.services.customer_service import get_customer_by_workshop, add_customer, update_customer_by_id, get_customer_by_id

router = APIRouter(prefix="/customers",tags=["customers"])


@router.post("", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(data: CustomerCreate, db:Annotated[Session,Depends(get_db)],user: Annotated[User,Depends(current_user_is_active)]):
    return add_customer(data=data,db=db,user=user)


@router.get("", response_model=List[CustomerRead])
def list_customers(db: Annotated[Session,Depends(get_db)], user: Annotated[User, Depends(current_user_is_active)]):
    customers = db.query(Customer).filter(Customer.shop_id == user.shop_id).order_by(Customer.id).all()
    return customers


@router.get("/by_document/{document_id}", response_model=CustomerRead)
def get_customer_by_document(document_id: str, db: Annotated[Session,Depends(get_db)], user: Annotated[User, Depends(current_user_is_active)]):
    return get_customer_by_workshop(document_id=document_id,db=db,user=user)

@router.get('/by_id/{customer_id}', response_model=CustomerRead)
def get_customer_id(
        customer_id: int,
        db: Annotated[Session,Depends(get_db)], user: Annotated[User,Depends(current_user_is_active)],
):
    return get_customer_by_id(id=customer_id,db=db,workshop=user.shop_id)

@router.get('/{customer_id}/details', response_model=CustomerReadDetail)
def get_customer_detail(
        customer_id: int,
        db: Annotated[Session,Depends(get_db)],
        user: Annotated[User,Depends(current_user_is_active)],
):
    result = db.query(Customer).filter(Customer.id == customer_id).first()
    return  result


@router.put("/{customer_id}", response_model=CustomerRead)
def update_customer(customer_id: int,payload: CustomerUpdate,db: Annotated[Session,Depends(get_db)],user: Annotated[User, Depends(current_user_is_active)]):
    return update_customer_by_id(customer_id=customer_id,db=db,payload=payload,current_user=user)

