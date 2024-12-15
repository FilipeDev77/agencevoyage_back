from fastapi import FastAPI
from dotenv import load_dotenv
import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from routes.signup import router as signup_router  # Importer depuis routes/signup.py
from pydantic import BaseModel
from db import get_db  # Importer depuis db.py
from routes.signin import router as login_router
from fastapi.middleware.cors import CORSMiddleware

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de la base de données
DATABASE_URL = os.getenv("DATABASE_URL")

# Configurer l'engine pour asyncpg
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Initialiser l'application FastAPI
app = FastAPI()

app = FastAPI()

# Ajouter le middleware CORS pour autoriser les requêtes provenant de n'importe quelle origine (vous pouvez restreindre aux origines spécifiques selon vos besoins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplacez "*" par les URLs spécifiques si vous souhaitez les restreindre
    allow_credentials=True,
    allow_methods=["*"],  # Cela permet d'autoriser toutes les méthodes (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Cela permet d'accepter tous les headers
)

# Ajouter le router d'utilisateurs
app.include_router(signup_router)  # Inclure le router de signup
app.include_router(login_router)

# Route de test de la connexion
@app.get("/test-connection")
async def test_connection():
    try:
        async with engine.connect() as conn:
            # Envoyer une requête simple
            result = await conn.execute(select(1))
            return {"success": True, "result": result.scalar()}
    except Exception as e:
        return {"success": False, "error": str(e)}
