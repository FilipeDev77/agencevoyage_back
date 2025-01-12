
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "une_chaine_super_secrete_que_personne_ne_connait"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 0.2


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) 
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    if "sub" not in payload: 
        raise HTTPException(status_code=401, detail="Utilisateur non autorisé")
    return payload["sub"]
