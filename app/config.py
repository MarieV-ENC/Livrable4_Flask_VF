import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

def to_bool(s):
    if s is None:
        return False
    return s.lower() == "true"

class Config:
    DEBUG = to_bool(os.environ.get("DEBUG"))
    SECRET_KEY = os.environ.get("SECRET_KEY") #suppression de  ,"dev"
    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        database=os.environ.get("DB_NAME")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    DETECTIONS_PER_PAGE = int(os.environ.get("DETECTIONS_PER_PAGE"))

def clean_arg(arg):
    if arg is None or arg.strip() == "":
        return None
    return arg.strip()