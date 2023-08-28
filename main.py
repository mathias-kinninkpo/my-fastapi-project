from fastapi import FastAPI
import models
from routes import router, router1
from config import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, tags=["Les actions sur les articles"])
app.include_router(router1, tags=["Les actions sur les utilisateurs"])

