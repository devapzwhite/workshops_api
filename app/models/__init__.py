from app.db.database import Base

# Importar todos los modelos
from app.models.user import User
from app.models.workshop import Workshop
from app.models.customer import Customer
from app.models.vehicle import Vehicle
from app.models.work_order import WorkOrder

__all__ = ["Base", "User", "Workshop", "Customer", "Vehicle", "WorkOrder"]
