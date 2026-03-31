# Import de Flask pour créer l'application
from flask import Flask

# Création de l'application Flask et définition des dossiers templates et fichiers statiques
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# Clé secrète utilisée pour les sessions et les messages Flash
app.secret_key = "dev"

# Import des routes de l'application
from app.routes import generales