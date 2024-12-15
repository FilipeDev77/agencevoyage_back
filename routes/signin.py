from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import bcrypt
from modeles.User_modele import User  
from shema.userlogin import UserLogin  
from db import get_db  

router = APIRouter()

@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
      
        result = await db.execute(select(User).where(User.username == user.username))
        db_user = result.scalars().first()


        if db_user and bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


