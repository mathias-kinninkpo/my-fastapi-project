from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from config import Base
Base = declarative_base()


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    image = Column(String(255))
    short_description = Column(String(255))
    description = Column(Text)
    author = Column(String(255))
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), default=None)



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(255))
    lastname = Column(String(255))
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    image = Column(String(255))
    code = Column(String(255))
    phone = Column(String(255), unique=True)
    email_verified_at = Column(DateTime(timezone=True))
    # is_active = Column(Boolean, default=True)
    # updated_at = Column(DateTime(timezone=True), onupdate=func.now())



    