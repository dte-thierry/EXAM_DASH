# Utilisez une image de base Python
FROM python:3.8-slim-buster

# Définissez un répertoire de travail
WORKDIR /appdash1

# Copiez les fichiers de requirements.txt dans le conteneur
COPY requirements.txt .

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le reste des fichiers du projet dans le conteneur
COPY . .

# Exposez le port sur lequel votre application s'exécutera
EXPOSE 8050

# Définissez la commande pour exécuter votre application
CMD ["python", "myDashboard.py"]
