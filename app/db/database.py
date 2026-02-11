from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2] #de la ubicacion de este archivo retrocede 2 veces para llegar al path raiz y encontrar el .env
ENV_PATH = BASE_DIR / ".env" #concatena el path raiz con el .env

load_dotenv(ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")

# Crea el engine que conecta con PostgreSQL
engine = create_engine(DATABASE_URL, echo=False)

# Cada request usara una sesion local para hablar con la db
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

# clase base de la cual heredaran todos los models o tablas
Base = declarative_base()