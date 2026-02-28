from contextlib import asynccontextmanager

from app import events
from fastapi import FastAPI

from app.api.v1 import vehicles, customers, workshops,auth,workOrder
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(vehicles.router)
app.include_router(customers.router)
app.include_router(workshops.router)
app.include_router(workOrder.router)

app.include_router(auth.router)



# Orígenes permitidos específicos
# origins = [
#     "http://localhost",
#     "http://localhost:8080",
#     "http://localhost:3000",
#     "http://192.168.1.84:3000",  # Tu IP local
#     "http://127.0.0.1:3000",
#     # Agregar más según necesites
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,  # Lista específica de orígenes
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],  # Métodos específicos
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"Hello": "World"}

