from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel
from models import Article
from datetime import datetime

T = TypeVar('T')

#################################################### les shemas pour les articles #################################################
class ArticleSchemaBase(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
   
    class Config:
        orm_mode = True
        from_attributes = True


class ArticleSchema(ArticleSchemaBase):
    is_public: Optional[bool] = None

class ArticleSchemaAll(ArticleSchemaBase):
       
     id : Optional[int] = None
     is_public: Optional[bool] = None
     created_at : Optional[T] = None
     updated_at : Optional[T] = None
     deleted_at : Optional[T] = None


# class Request(GenericModel, Generic[T]):
#     parameter: Optional[T] = Field(...)


class RequestArticle(ArticleSchema):
    pass


class RequestArticleGet(ArticleSchemaBase):
    pass


class Response(GenericModel, Generic[T]):
    code: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None
    result: Optional[T] = None
    token : Optional[str] = None

#################################################### les shemas pour les Users #################################################


class UserBase(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    image: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int
    code: Optional[str] = None
    email_verified_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True
