from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel
from models import Article
from datetime import datetime

T = TypeVar('T')


class ArticleSchema(BaseModel):
    id: Optional[int]
    title: Optional[str] = None
    image: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    is_public: Optional[bool] = None
    created_at : Optional[datetime] = None
    updated_at : Optional[datetime] = None
    deleted_at : Optional[datetime] = None

    class Config:
        orm_mode = True


class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)


class RequestArticle(BaseModel):
    parameter: ArticleSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None
    result: Optional[T] = None