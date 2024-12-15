from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import bcrypt
from modeles.User_models import User
from shema.Usercreate import UserSchema  # Assurez-vous que UserSchema est bien défini
from db import get_db  # Importer depuis db.py

# Créer un router pour les routes liées aux utilisateurs
router = APIRouter()

@router.post("/signup")
async def signup(user: UserSchema, db: AsyncSession = Depends(get_db)):
    try:
       

        # Hacher le mot de passe
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

        # Créer un nouvel utilisateur
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
