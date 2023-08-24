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
async def create_article_service(request: RequestArticle, db: Session = Depends(get_db)):
    crud.create_article(db,article=request.parameter)
    return Response(status="Ok",
                    code="200",
                    message="Article created successfully").dict(exclude_none=True)


@router.get("/")
async def get_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    _articles = crud.get_article(db, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_articles)

@router.get("/{id}")
async def get_article(db: Session = Depends(get_db), id: int = 0):
    _articles = crud.get_article_by_id(db, id)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_articles)


@router.patch("/update")
async def update_article(request: RequestArticle, db: Session = Depends(get_db)):
    _article = crud.update_article(db,id = request.parameter.id, title=request.parameter.title, short_description=request.parameter.short_description, description= request.parameter.description, image=request.parameter.image, author=request.parameter.author, is_public=request.parameter.is_public)
    return Response(status="Ok", code="200", message="Success update data", result=_article)


@router.delete("/delete/{id}")
async def delete_article(db: Session = Depends(get_db), id : int = None):
    crud.remove_article(db,id=id)
    return Response(status="Ok", code="200", message="Success delete data").dict(exclude_none=True)