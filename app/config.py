# Import du module os pour accéder aux variables d'environnement et aux chemins
import os

# Import de load_dotenv pour charger automatiquement le fichier .env
from dotenv import load_dotenv

# Import de URL pour construire proprement l'URL de connexion à la base de données
from sqlalchemy.engine import URL

# Import de Path pour manipuler des chemins de fichiers
from pathlib import Path

# Récupération du dossier racine du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Chargement du fichier .env situé à la racine du projet
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Fonction transformant une chaîne de caractères en booléen
def to_bool(s):
    # Si aucune valeur n'est fournie, on retourne False
    if s is None:
        return False

    # Retourne True uniquement si la chaîne vaut "true"
    return s.lower() == "true"

# Classe contenant toute la configuration de l'application
class Config:
    # Active ou non le mode debug selon la variable d'environnement DEBUG
    DEBUG = to_bool(os.environ.get("DEBUG"))

    # Clé secrète utilisée par Flask pour les sessions et la sécurité
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Construction de l'URL de connexion à la base PostgreSQL
    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        database=os.environ.get("DB_NAME")
    )

    # Désactive le suivi automatique des modifications de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Nombre d'éléments affichés par page dans la pagination
    DETECTIONS_PER_PAGE = int(os.environ.get("DETECTIONS_PER_PAGE"))

# Fonction supprimant les espaces inutiles dans un argument
def clean_arg(arg):
    # Si l'argument est vide ou contient uniquement des espaces, on retourne None
    if arg is None or arg.strip() == "":
        return None

    # Sinon on retourne la valeur sans les espaces au début et à la fin
    return arg.strip()