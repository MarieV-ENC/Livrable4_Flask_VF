# Import de Flask pour créer l'application
from flask import Flask

# Import de SQLAlchemy pour gérer la base de données avec un ORM
from flask_sqlalchemy import SQLAlchemy

# Import de la configuration de l'application
from .config import Config

# Import de la protection CSRF pour sécuriser les formulaires
from flask_wtf.csrf import CSRFProtect

# Chargement des variables d'environnement depuis le fichier .env
from dotenv import load_dotenv  # ajout test

# Création de l'application Flask et définition des dossiers templates et static
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# Chargement de la configuration définie dans Config
app.config.from_object(Config)

# Clé secrète désormais définie dans Config
# app.secret_key = "dev" voir si suppression crée bug

# Initialisation de la base de données liée à l'application
db = SQLAlchemy(app)

# Activation de la protection CSRF sur tous les formulaires
csrf = CSRFProtect(app)

# Import des routes pour enregistrer les différentes pages de l'application
from app.routes import generales