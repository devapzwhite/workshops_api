from typing import List, Annotated

from fastapi import APIRouter, status, Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.customer import CustomerRead, CustomerCreate
from app.models.customer import Customer

router = APIRouter(prefix="/customers",tags=["customers"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(data: CustomerCreate, db:Annotated[Session,Depends(get_db)]): # implementar: debe recibir el token por header
    existing = db.query(Customer).filter(Customer.document_id == data.document_id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Customer with that document_id already exists")
    customer = Customer(
        document_id=data.document_id,
        name=data.name,
        last_name=data.last_name,
        phone=data.phone,
        email=data.email,
        address=data.address,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get("/", response_model=List[CustomerRead])
def list_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).order_by(Customer.id).all()
    return customers

@router.get("/{customer_rut}", response_model=CustomerRead)
def get_customer_by_id(customer_rut: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.document_id == customer_rut).first()
    return customer