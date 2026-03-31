# Import des outils de gestion de connexion utilisateur
from flask_login import LoginManager, UserMixin

# Import des fonctions permettant de sécuriser les mots de passe
from werkzeug.security import generate_password_hash, check_password_hash

# Import de l'application Flask et de la base de données
from ..app import app, db

# Initialisation du gestionnaire de connexion
login_manager = LoginManager()

# Association du système de connexion à l'application Flask
login_manager.init_app(app)

# Page vers laquelle l'utilisateur est redirigé s'il n'est pas connecté
login_manager.login_view = "login"


# Modèle représentant les utilisateurs de l'application
class User(UserMixin, db.Model):
    __tablename__ = "user_account"
    __table_args__ = {"schema": "crec"}

    # Identifiant unique de l'utilisateur
    user_id = db.Column(db.Integer, primary_key=True)

    # Nom d'utilisateur unique
    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    # Adresse e-mail unique
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    # Mot de passe stocké sous forme chiffrée
    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    # Petite description ou biographie de l'utilisateur
    bio = db.Column(db.Text)

    # Relation entre un utilisateur et ses commentaires
    comments = db.relationship(
        "Comment",
        backref="author",
        lazy=True
    )

    # Retourne l'identifiant utilisé par Flask-Login
    def get_id(self):
        return str(self.user_id)

    # Transforme le mot de passe en hash avant de l'enregistrer
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Vérifie si le mot de passe saisi correspond au hash enregistré
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Fonction utilisée par Flask-Login pour retrouver un utilisateur connecté
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))