# Import de datetime pour enregistrer automatiquement la date de création
from datetime import datetime

# Import de l'objet db contenant la connexion et les modèles SQLAlchemy
from ..app import db

# Mapping de la table des commentaires de la base de données
class Comment(db.Model):
    # Nom de la table dans la base
    __tablename__ = "comment"

    # Schéma dans lequel se trouve la table
    __table_args__ = {"schema": "crec"}

    # Identifiant unique du commentaire
    comment_id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Contenu textuel du commentaire
    content = db.Column(
        db.Text,
        nullable=False
    )

    # Date et heure de création du commentaire
    # La valeur est générée automatiquement lors de l'ajout
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Identifiant de l'utilisateur ayant écrit le commentaire
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("crec.user_account.user_id"),
        nullable=False
    )

    # Identifiant du faucon auquel le commentaire est associé
    falcon_id = db.Column(
        db.Integer,
        db.ForeignKey("crec.falcon.falcon_id"),
        nullable=False
    )