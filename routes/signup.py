from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import bcrypt
from modeles.User_models import User
from shema.Usercreate import UserSchema 
from db import get_db  


router = APIRouter()

@router.post("/signup")
async def signup(user: UserSchema, db: AsyncSession = Depends(get_db)):
    try:
       

       
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

      
        new_user = User(
            username=user.username,
            password=hashed_password.decode("utf-8"),
            address=user.address,
            phone=user.phone,
            country=user.country,
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return {"message": "User created successfully", "user_id": new_user.id_user}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
