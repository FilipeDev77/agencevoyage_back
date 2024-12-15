from unittest.mock import Base


from sqlalchemy import create_engine


from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)