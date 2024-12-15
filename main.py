from fastapi import FastAPI
from dotenv import load_dotenv
import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from routes.signup import router as signup_router  # Importer depuis routes/signup.py

from routes.signin import router as login_router
from fastapi.middleware.cors import CORSMiddleware
from routes.info_user import router as infos_user_router
# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de la base de données
DATABASE_URL = os.getenv("DATABASE_URL")

# Configurer l'engine pour asyncpg
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Initialiser l'application FastAPI
app = FastAPI()

origins = [
    "http://localhost:5173",  # Frontend
    "http://localhost:3000",  # Si vous utilisez un autre port pour le frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Ajouter une origine spécifique
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ajouter le router d'utilisateurs
app.include_router(signup_router)  # Inclure le router de signup
app.include_router(login_router)
app.include_router(infos_user_router)

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
