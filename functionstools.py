from config import SessionLocal
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException, Header

# Configuration pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Configuration pour la génération et la validation des JWT
SECRET_KEY = "codesecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Fonction pour créer un token d'accès
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm =ALGORITHM)
    return encoded_jwt


def get_token(authorization: str = Header(default=None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    print(authorization)
    if authorization.startswith("Bearer "):
        token = authorization[7:]
        return token
    
    raise HTTPException(status_code=401, detail="Invalid authorization header")



# Fonction de vérification du mot de passe
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Fonction de génération du hachage du mot de passe
def get_password_hash(password):
    return pwd_context.hash(password)

# Fonction de décodage du token
def decode_token(token : str):
    try:
        payload : dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub", None)
        exp = payload.get("exp", None)
        print(payload)
        if username is None or exp is None:
            return None
        # if int(exp) - datetime.utcnow().second() <= 0:
        #     return "expired"
        token_data = username 
        return token_data
    except :
        return None
