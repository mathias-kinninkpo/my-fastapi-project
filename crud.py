from sqlalchemy.orm import Session
from models import Article
from schemas import ArticleSchema
from fastapi import HTTPException


def get_article(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Article).offset(skip).limit(limit).all()


def get_article_by_id(db: Session, id: int):
    return db.query(Article).filter(Article.id == id).first()


def create_article(db: Session, article: ArticleSchema):
    _article = Article(title=article.title, short_description=article.short_description, description= article.description, image=article.image, author=article.author, is_public=article.is_public)
    db.add(_article)
    db.commit()
    db.refresh(_article)
    return _article


def remove_article(db: Session, id: int):
    _article = get_article_by_id(db=db, id= id)

    if _article is not None:
       db.delete(_article)
       db.commit()
    else:
        raise HTTPException(status_code=404, detail="article not found")
    return _article
    


def update_article(db: Session, id: int, title: str, short_description : str, description : str, image: str, author : str, is_public: bool):
    _article = get_article_by_id(db=db, id = id)
    if _article is not None:
        _article.title = title
        _article.short_description = short_description, 
        _article.description = description
        _article.image = image
        _article.author = author
        _article.is_public = is_public

        db.commit()
        db.refresh(_article)
    else:
        raise HTTPException(status_code=404, detail="article not found")
    return _article