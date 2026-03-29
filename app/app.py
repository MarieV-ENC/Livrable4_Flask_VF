from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv # ajout test

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config.from_object(Config)

# app.secret_key = "dev" voir si suppression crée bug

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

from app.routes import generales