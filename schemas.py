from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class ArticleSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    image: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    is_public: Optional[bool] = None

    class Config:
        orm_mode = True


class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)


class RequestArticle(BaseModel):
    parameter: ArticleSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]