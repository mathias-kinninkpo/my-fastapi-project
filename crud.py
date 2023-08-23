from sqlalchemy.orm import Session
from models import Article
from schemas import ArticleSchema


def get_article(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Article).offset(skip).limit(limit).all()


def get_article_by_id(db: Session, article_id: int):
    return db.query(Article).filter(Article.id == article_id).first()


def create_article(db: Session, article: ArticleSchema):
    _article = article(title=article.title, description=article.description)
    db.add(_article)
    db.commit()
    db.refresh(_article)
    return _article


def remove_article(db: Session, article_id: int):
    _article = get_article_by_id(db=db, article_id=article_id)
    db.delete(_article)
    db.commit()


def update_article(db: Session, article_id: int, title: str, description: str):
    _article = get_article_by_id(db=db, article_id=article_id)

    _article.title = title
    _article.description = description

    db.commit()
    db.refresh(_article)
    return _article