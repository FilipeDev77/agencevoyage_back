from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    password: str
    address: str
    phone: str
    country: str

    class Config:
        orm_mode = True