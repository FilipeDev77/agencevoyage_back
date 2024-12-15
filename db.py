from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de la base de données
DATABASE_URL = os.getenv("DATABASE_URL")

# Configurer l'engine pour asyncpg
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Dépendance pour la session de base de données
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
