from typing import Optional,List

from fastapi import FastAPI

from app.api.v1 import vehicles, customers, workshops,auth
from pydantic import BaseModel, EmailStr


app = FastAPI()
app.include_router(vehicles.router)
app.include_router(customers.router)
app.include_router(workshops.router)

app.include_router(auth.router)



@app.get("/")
def read_root():
    return {"Hello": "World"}


class customerBase(BaseModel):
    document_id: str
    name: str
    last_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
