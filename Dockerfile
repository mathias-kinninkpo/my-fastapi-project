# Utilisez une image Python officielle
FROM python:3.8-slim

# Définissez le répertoire de travail dans le conteneur
WORKDIR .

# Copiez le fichier requirements.txt dans le conteneur
COPY requirements.txt requirements.txt

# Installez les dépendances
RUN pip install -r requirements.txt

# Copiez le reste du code source dans le conteneur
COPY . .

# Exposez le port utilisé par FastAPI
EXPOSE 8000

# Lancez l'application FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

