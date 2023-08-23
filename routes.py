from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import ArticleSchema, Request, Response, RequestArticle

import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
async def create_book_service(request: RequestArticle, db: Session = Depends(get_db)):
    crud.create_Article(db,article=request.parameter)
    return Response(status="Ok",
                    code="200",
                    message="Article created successfully").dict(exclude_none=True)


@router.get("/")
async def get_Articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _Articles = crud.get_article(db, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_Articles)


@router.patch("/update")
async def update_Article(request: RequestArticle, db: Session = Depends(get_db)):
    _Article = crud.update_article(db,article_id=request.parameter.id,
                             title=request.parameter.title, description=request.parameter.description)
    return Response(status="Ok", code="200", message="Success update data", result=_Article)


@router.delete("/delete")
async def delete_article(request: RequestArticle,  db: Session = Depends(get_db)):
    crud.remove_Article(db,article_id=request.parameter.id)
    return Response(status="Ok", code="200", message="Success delete data").dict(exclude_none=True)