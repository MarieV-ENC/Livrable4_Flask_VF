# Import de FlaskForm pour créer des formulaires sécurisés avec Flask-WTF
from flask_wtf import FlaskForm

# Import des différents types de champs utilisés dans les formulaires
from wtforms import StringField, SelectField, DateField, TextAreaField

# Import du validateur Optional pour rendre certains champs facultatifs
from wtforms.validators import Optional


# Formulaire de recherche avancée dans la base
class Recherche(FlaskForm):

    # Liste déroulante contenant les codes des faucons
    code_faucon = SelectField(
        "falcon_code",
        choices=[],
        validators=[Optional()]
    )

    # Champ permettant de filtrer les résultats par date
    date_filtre = DateField(
        "Date",
        validators=[Optional()],
        format='%Y-%m-%d'
    )

    # Champ texte permettant de rechercher un lieu
    place = StringField(
        "space_label",
        validators=[Optional()]
    )


# Formulaire utilisé pour modifier le nom d'un faucon
class Modification(FlaskForm):

    # Liste déroulante pour choisir le faucon à modifier
    code_faucon = SelectField(
        "falcon_code",
        choices=[],
        validators=[Optional()]
    )

    # Champ texte contenant le nouveau nom du faucon
    nom_faucon = StringField(
        "nom_faucon",
        validators=[]
    )

    # Zone de texte utilisée pour enregistrer la modification
    update = TextAreaField(
        "code_faucon",
        validators=[]
    )