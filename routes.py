from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import ArticleSchemaAll, Request, Response, RequestArticle, RequestArticleGet

import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/articles")
async def create_article_service(request: RequestArticleGet, db: Session = Depends(get_db)):
    crud.create_article(db,article=request)
    return Response(status="Ok",
                    code="200",
                    message="Article created successfully").dict(exclude_none=True)


@router.get("/articles")
async def get_articles(db: Session = Depends(get_db)):
    _articles = crud.get_article(db)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_articles)




@router.get("/articles/{id}")
async def get_article(db: Session = Depends(get_db), id: int = 0):
    _articles = crud.get_article_by_id(db, id)
    if _articles is not None:
        return Response(status="Ok", code="200", message="Success fetch all data", result= ArticleSchemaAll.from_orm(_articles))
    
    raise HTTPException(status_code=404, detail="Article not found")




@router.get("/public/articles")
async def get_public_articles(db: Session = Depends(get_db)):
    _articles = crud.get_public_article(db)
    return Response(status="Ok", code="200", message="Success feth all public article", result=_articles)



@router.get("/private/articles")
async def get_private_articles(db: Session = Depends(get_db)):
    _articles = crud.get_private_article(db)
    return Response(status="Ok", code="200", message="Success feth all private article", result=_articles)

@router.patch("/articles/{id}")
async def update_article(id: int , request: RequestArticle, db: Session = Depends(get_db)):
    _article = crud.update_article(db,id = id , title=request.title, short_description=request.short_description, description= request.description, image=request.image, author=request.author, is_public=request.is_public)
    return Response(status="Ok", code="200", message="Success update data", result=_article)




@router.delete("articles/{id}")
async def delete_article(db: Session = Depends(get_db), id : int = None):
    crud.remove_article(db,id=id)
    return Response(status="Ok", code="200", message="Success delete data").dict(exclude_none=True)



