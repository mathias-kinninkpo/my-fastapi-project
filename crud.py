from sqlalchemy.orm import Session
from models import Article, User
from schemas import ArticleSchemaAll, ArticleSchema, UserSchema, UserCreate, UserUpdate
from fastapi import HTTPException, status
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string




def generate_verification_code(length=6):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code


def send_verification_code_email(email: str, code: str, message: str):
    sender_email = "0dc70c4667bbe7"  
    sender_password = "3055376bcb5bb7"  
    recipient_email = email
    subject = "Code de verification"
    mes = f"{message}: {code}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(mes, "plain"))

    try:
        server = smtplib.SMTP("sandbox.smtp.mailtrap.io", 587)  
        server.starttls()
        server.login(sender_email, sender_password)
        senders = server.sendmail(sender_email, recipient_email, msg.as_string())
        print(senders)
        print(recipient_email)
        server.quit()
        return True
    except:
        return False



################################ les routes pour les articles #################################


def get_article(db: Session):
    articles = db.query(Article).filter(Article.deleted_at == None).all()
    return  [ArticleSchemaAll.from_orm(article) for article in articles]


def get_public_article(db: Session):
    articles = db.query(Article).filter((Article.deleted_at == None) & (Article.is_public == True)).all()
    return  [ArticleSchemaAll.from_orm(article) for article in articles]


def get_private_article(db: Session):
    articles = db.query(Article).filter((Article.deleted_at == None) & (Article.is_public != True)).all()
    return  [ArticleSchemaAll.from_orm(article) for article in articles]



def get_article_by_id(db: Session, id: int):
    return db.query(Article).filter((Article.id == id ) & (Article.deleted_at == None)).first()
    
    

def create_article(db: Session, article: ArticleSchema):
    _article = Article(title=article.title, short_description=article.short_description, description= article.description, image=article.image, author=article.author)
    db.add(_article)
    db.commit()
    db.refresh(_article)
    return ArticleSchemaAll.from_orm(_article)


def remove_article(db: Session, id: int):
    _article = get_article_by_id(db=db, id= id)
    
    if _article is not None:
       _article.deleted_at = datetime.now()
       db.commit()
       db.refresh(_article)
    else:
        raise HTTPException(status_code=404, detail="article not found")
    return ArticleSchemaAll.from_orm(_article)
    


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
    return ArticleSchemaAll.from_orm(_article)


################################ les routes pour les utilisateurs #################################

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    if send_verification_code_email(user.email, user.code, "Le code de verification pour la creation de votre compte est "):
        _user = User(   firstname = user.firstname,
                        lastname = user.lastname,
                        email = user.email,
                        image = user.image,
                        phone = user.phone,
                        username = user.username,
                        password=hashed_password, 
                        code = generate_verification_code()
                    )
        try:
            db.add(_user)
            db.commit()
            db.refresh(_user)
            return _user
        except IntegrityError:  
            db.rollback()
            return None
    return None


def authenticate_user(db: Session, email: str, password: str):
    _user = get_user_by_email(db, email)
    if not _user is None:
        try:
            # hashed_password = pwd_context.hash(password)
            if pwd_context.verify(password, _user.password, schemes=["bcrypt"]):
                return _user
            return None
        except:
            return None
        
    return None
   


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()




# Fonction pour vérifier le code de vérification lors de l'inscription
def register_verify(db: Session, email: str, code: str):
    user = db.query(User).filter(User.email == email, User.code == code).first()
    if user:
        user.email_verified_at = datetime.now()
        db.commit()
        db.refresh(user)
        return True
    return False






def password_forgot(db: Session, email: str):
    user = get_user_by_email(db, email)
    if user:
        new_code = generate_verification_code()
        user.code = new_code
        db.commit()
        if send_verification_code_email(email, new_code, "Le code de verification pour changer votre mot de passe est "):
            return user
    return None

# Fonction pour vérifier le code de vérification lors de la réinitialisation de mot de passe
def password_forgot_verify(db: Session, email: str, code: str):
    user = db.query(User).filter(User.email == email, User.code == code).first()
    if user:
        user.email_verified_at = datetime.now()
        db.commit()
        db.refresh(user)
    return None



def update_profile(db: Session, user_id: int, updated_user: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        try:
            for field, value in updated_user.dict().items():
                if field == 'password':
                    hashed_password = pwd_context.hash(user.password)
                    setattr(user, field, hashed_password)
                else:
                    setattr(user, field, value)
            db.commit()
            db.refresh(user)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = str(e))
        return user
    return None


