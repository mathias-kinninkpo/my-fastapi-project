from fastapi import APIRouter, HTTPException, Path, status
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import (   ArticleSchemaAll, 
                        Response, 
                        RequestArticle, 
                        RequestArticleGet, 
                        UserSchema,
                        UserCreate, 
                        UserUpdate
                    )

import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()






########################################### Les routes pour les articles ##################################################

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





########################################### Les routes pour les utilisateurs ##################################################

router1 = APIRouter()


@router1.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    _result = {'code': db_user.code}
    if db_user:
        return Response(status="Ok", code="200", message="Successfull regsitered user and email sent successfully", result = _result).dict(exclude_none=True)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email or password already exists")


@router1.post("/register/verify")
async def register(email : str, code :str, db: Session = Depends(get_db)):
    db_user = crud.register_verify(email=email, code=code, db=db)
    if db_user:
        return Response(status="Ok", code="200", message="Successfull regsitered user").dict(exclude_none=True)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="L'email ou le username entré existe déjà")


@router1.get("/users/{id}")
async def read_user(id: int, db: Session = Depends(get_db)):
    _user = crud.get_user(db, id)
    if not _user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return Response(status="Ok", code="200", message="Succes fetch profile", result = UserSchema.from_orm(_user))


@router1.patch("/users/{id}")
async def update_profile(user : UserUpdate, id: int, db : Session = Depends(get_db)):
    _user = crud.update_profile(db,user_id = id, updated_user = user)
    if _user is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or credentials already exist")
    else:
        return  Response(status="Ok", code="200", message="Profile updated successfull").dict(exclude_none=True)



@router1.post("/login")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, email = email, password = password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return  Response(status="Ok", code="200", message="Authentification verified").dict(exclude_none=True)


# @router1.get("/profile/{id}")
# async def profile(id: int, db : Session = Depends(get_db)):
#     _user = crud.get_user(db,id = id )
#     return Response(status="Ok", code="200", message="Succes fetch profile", result = UserSchema.from_orm(_user))



@router1.post("/password/forgot")
async def forgot_password(email: str, db: Session = Depends(get_db)):
    user = crud.password_forgot(db, email)
    _result = {'code': user.code}
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return  Response(status="Ok", code="200", message="email sent", result = _result).dict(exclude_none=True)


@router1.post("/password/forgot/verify")
async def verify_forgot_password(email: str, code: str, db: Session = Depends(get_db)):
    user = crud.password_forgot_verify(db, email, code)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return  Response(status="Ok", code="200", message="Authentification verified").dict(exclude_none=True)







