from fastapi import FastAPI
from dotenv import load_dotenv
import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from routes.signup import router as signup_router  

from routes.signin import router as login_router
from fastapi.middleware.cors import CORSMiddleware
from routes.info_user import router as infos_user_router

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


app = FastAPI()

origins = [
  
    "http://localhost:3000",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(signup_router)
app.include_router(login_router)
app.include_router(infos_user_router)


@app.get("/test-connection")
async def test_connection():
    try:
        async with engine.connect() as conn:
            
            result = await conn.execute(select(1))
            return {"success": True, "result": result.scalar()}
    except Exception as e:
        return {"success": False, "error": str(e)}
