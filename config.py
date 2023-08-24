from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Charge les variables d'environnement depuis le fichier .env

DATABASE_URL = "postgresql://mathias:AfdWCPQAH7J6bFsBo3YNRqU5r895G0cn@dpg-cjjoqgr37aks738econg-a.oregon-postgres.render.com/gestion_pjt0"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind=engine)
Base = declarative_base()