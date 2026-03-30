# Configuration flaskWTF pour formulaires

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField
from wtforms.validators import Optional

# formulaires avancée d'interrogation

class Recherche(FlaskForm):
    code_faucon = SelectField("falcon_code", choices=[], validators=[Optional()])
    date_filtre  = DateField("Date", validators=[Optional()], format='%Y-%m-%d')
    place = StringField("space_label", validators=[Optional()])

# formulaire de modification des noms de faucons

class Modification(FlaskForm):
    code_faucon = SelectField("falcon_code", choices=[], validators=[Optional()])
    nom_faucon = StringField("nom_faucon", validators=[ ])
    update = TextAreaField("code_faucon", validators=[])    