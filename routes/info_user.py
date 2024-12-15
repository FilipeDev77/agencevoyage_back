from modeles.User_models import User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from security.token import get_current_user
from db import get_db


from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


router = APIRouter()

@router.get("/info_user")
async def get_info_user(current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        # Exécuter la requête pour récupérer les informations de l'utilisateur
        result = await db.execute(select(User).where(User.username == current_user))
        
        # Récupérer le premier utilisateur correspondant
        db_user = result.scalars().first()

        # Si aucun utilisateur n'est trouvé, retourner un message d'erreur
        if db_user is None:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

        # Retourner les informations de l'utilisateur sous forme de dictionnaire
        return {column.name: getattr(db_user, column.name) for column in User.__table__.columns}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur : {str(e)}")

