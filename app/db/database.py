import re
from app.core.config import Settings

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from pathlib import Path
from sqlalchemy.ext.asyncio import async_sessionmaker
BASE_DIR = Path(__file__).resolve().parents[2] #de la ubicacion de este archivo retrocede 2 veces para llegar al path raiz y encontrar el .env
ENV_PATH = BASE_DIR / ".env" #concatena el path raiz con el .env


settings = Settings()

raw_url = settings.DATABASE_URL
DATABASE_URL = re.sub(
    r"^postgresql(\+\w+)?://",
    "postgresql+asyncpg://",
    raw_url
)

# Elimina parámetros que asyncpg no soporta en la URL
DATABASE_URL = re.sub(r"[?&]sslmode=\w+", "", DATABASE_URL)
DATABASE_URL = re.sub(r"[?&]channel_binding=\w+", "", DATABASE_URL)
# Crea el engine que conecta con PostgreSQL
engine = create_async_engine(DATABASE_URL, echo=False)

# Cada request usara una sesion local para hablar con la db
SessionLocal = async_sessionmaker(engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False)

# clase base de la cual heredaran todos los models o tablas
Base = declarative_base()
async def get_db():
    async with SessionLocal() as session:
        yield session