from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

# Import des modèles de données principaux
from ..models.crec import Falcon, Bird_detection, Place, Weather_station, Weather_measurement
from ..models.comment import Comment
from ..models.users import User

# Import de l'application Flask et de la session SQLAlchemy
from ..app import app, db

from sqlalchemy import or_, text
from flask import current_app

# Import des formulaires Flask-WTF
from ..models.formulaires import Recherche
from ..config import clean_arg
from ..models.formulaires import Recherche, Modification

# Import des outils de gestion des dates
from datetime import datetime
from datetime import datetime, timedelta

import os
import json
import csv

# Route de la page d'accueil
@app.route("/")
def index():    
    return render_template("index.html")


# Route de la page carte
@app.route("/map")
def map_page():
    return render_template("map.html")


# Page de recherche avec formulaire vide
@app.route("/search")
def search():

    # Initialisation du formulaire
    formulaire_oiseau = Recherche()

    # Récupération des codes de faucons pour alimenter la liste déroulante
    falcons = Falcon.query.order_by(Falcon.falcon_code).all()
    formulaire_oiseau.code_faucon.choices = [('', '-- Tous --')] + [
        (f.falcon_code, f.falcon_code)
        for f in falcons
    ]

    return render_template("search.html", form=formulaire_oiseau)


# Connexion utilisateur
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_value = request.form["login"]
        password = request.form["password"]

        # Recherche par nom d'utilisateur ou adresse mail
        user = User.query.filter(
            (User.username == login_value) | (User.email == login_value)
        ).first()

        # Vérification du mot de passe puis ouverture de session
        if user and user.check_password(password):
            login_user(user)
            flash("Connexion réussie.")
            return redirect(url_for("profile"))

        flash("Identifiants incorrects.")
        return redirect(url_for("login"))

    return render_template("login.html")


# Inscription d'un nouvel utilisateur
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        bio = request.form.get("bio", "").strip()

        # Vérification de la confirmation du mot de passe
        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.")
            return redirect(url_for("register"))

        # Vérification de l'unicité du nom d'utilisateur
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash("Cet identifiant existe déjà.")
            return redirect(url_for("register"))

        # Vérification de l'unicité de l'adresse mail
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("Cette adresse mail existe déjà.")
            return redirect(url_for("register"))

        # Création du nouvel utilisateur
        user = User(
            username=username,
            email=email, 
            bio=bio
        )
        user.set_password(password)

        # Enregistrement dans la base
        db.session.add(user)
        db.session.commit()

        flash("Compte créé. Vous pouvez vous connecter.")
        return redirect(url_for("login"))

    return render_template("register.html")


# Déconnexion d'un utilisateur connecté
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.")
    return redirect(url_for("index"))


# Fiche détaillée d'un faucon
@app.route("/bird/<falcon_id>", methods=["GET", "POST"])
def bird_detail(falcon_id):

    # Recherche du faucon à partir de son code
    falcon = Falcon.query.filter_by(falcon_code=falcon_id).first()
    bird = None

    if falcon:
        # Préparation des données affichées dans la fiche
        bird = {
            'falcon_id': falcon_id,
            'falcon_code': falcon_id,
            'nickname': falcon.nickname if falcon.nickname else falcon_id,
            'tag_id': falcon.tag_id,
            'espece': 'Non renseignée'
        }

    # Ajout d'un commentaire par un utilisateur connecté
    if request.method == "POST" and current_user.is_authenticated:
        content = request.form.get("comment", "").strip()
        if content and falcon:
            comment = Comment(
                content=content,
                user_id=current_user.user_id,
                falcon_id=falcon.falcon_id
            )
            db.session.add(comment)
            db.session.commit()
            flash("Commentaire publié.")
        return redirect(url_for("bird_detail", falcon_id=falcon_id))

    # Récupération des commentaires du faucon du plus récent au plus ancien
    comments = []
    if falcon:
        comments = Comment.query.filter_by(
            falcon_id=falcon.falcon_id
        ).order_by(Comment.created_at.desc()).all()

    return render_template("bird_detail.html", bird=bird, comments=comments)


# Profil de l'utilisateur connecté
@app.route("/profile")
@login_required
def profile():
    comments = Comment.query.filter_by(
        user_id=current_user.user_id
    ).order_by(
        Comment.created_at.desc()
    ).all()

    return render_template(
        "profile.html",
        comments=comments
    )


# Pages statiques
@app.route("/methodology")
def methodology():
    return render_template("methodology.html")


@app.route("/dataviz")
def dataviz():
    return render_template("dataviz.html")


@app.route("/legal")
def legal():
    return render_template("legal.html")


# Gestion personnalisée des erreurs 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# Recherche avancée avec filtres et pagination
@app.route("/recherche", methods=['GET'])
@app.route("/recherche/<int:page>", methods=['GET'])
def recherche(page=1):
    form = Recherche()

    # Chargement des codes de faucons dans la liste déroulante
    falcons = Falcon.query.order_by(Falcon.falcon_code).all()
    form.code_faucon.choices = [('', '-- Tous --')] + [
        (f.falcon_code, f.falcon_code)
        for f in falcons
    ]

    # Récupération et nettoyage des filtres saisis
    code_faucon = clean_arg(request.args.get("code_faucon", None))
    date_filtre = clean_arg(request.args.get("date_filtre", None))
    place_filtre = clean_arg(request.args.get("place", None))

    # Conversion de la date saisie en objet date
    date_obj = None
    if date_filtre:
        try:
            date_obj = datetime.strptime(date_filtre, "%Y-%m-%d").date()
        except ValueError:
            pass

    # Préremplissage du formulaire avec les valeurs déjà saisies
    form.code_faucon.data = code_faucon
    form.date_filtre.data = date_obj
    form.place.data = place_filtre

    donnees = []

    # Construction progressive de la requête SQLAlchemy
    if code_faucon or date_obj or place_filtre:
        query_results = db.session.query(Bird_detection)

        # Filtre sur le code du faucon
        if code_faucon:
            query_results = query_results.join(
                Falcon, Falcon.falcon_id == Bird_detection.falcon_id
            ).filter(
                Falcon.falcon_code.ilike("%" + code_faucon.lower() + "%")
            )

        # Filtre sur une journée complète
        if date_obj:
            from datetime import time
            debut = datetime.combine(date_obj, time(0, 0, 0))
            fin = datetime.combine(date_obj + timedelta(days=1), time(0, 0, 0))
            query_results = query_results.filter(
                Bird_detection.time >= debut,
                Bird_detection.time < fin
            )

        # Filtre sur le lieu
        if place_filtre:
            query_results = query_results.join(
                Place, Place.place_id == Bird_detection.place_id
            ).filter(
                Place.space_label.ilike("%" + place_filtre.lower() + "%")
            )

        # Tri et pagination des résultats
        donnees = query_results \
            .order_by(Bird_detection.time) \
            .paginate(page=page, per_page=app.config["DETECTIONS_PER_PAGE"])

    return render_template("search.html",
            sous_titre="Recherche",
            donnees=donnees,
            form=form)


# Liste des faucons et modification de leur surnom
@app.route("/birds", methods=['GET', 'POST'])
def birds():
    form = Modification()

    # Chargement des faucons dans le formulaire
    falcons = Falcon.query.order_by(Falcon.falcon_code).all()
    form.code_faucon.choices = [('', '-- Tous --')] + [
        (f.falcon_code, f.nickname if f.nickname else f.falcon_code)
        for f in falcons
    ]

    # Mise à jour du surnom d'un faucon
    if form.validate_on_submit():
        code_faucon = clean_arg(request.form.get("code_faucon", None))
        nom_faucon = clean_arg(request.form.get("nom_faucon", None))

        falcon = Falcon.query.filter_by(falcon_code=code_faucon).first()

        if falcon:
            falcon.nickname = nom_faucon
            db.session.commit()
            flash(f"Surnom « {nom_faucon} » enregistré pour {code_faucon}.")
        else:
            flash(f"Faucon introuvable : {code_faucon}.", "warning")

        return redirect(url_for("birds"))

    # Préparation des données à afficher dans les fiches oiseaux
    couleurs = [
        '#e41a1c', '#377eb8', '#4daf4a', '#984ea3',
        '#ff7f00', '#a65628', '#f781bf', '#999999',
        '#17becf', '#bcbd22', '#ff9896', '#aec7e8'
    ]

    oiseaux = []
    for i, falcon in enumerate(falcons):
        oiseaux.append({
            'falcon_id': falcon.falcon_code,
            'falcon_code': falcon.falcon_code,
            'nickname': falcon.nickname if falcon.nickname else falcon.falcon_code,
            'tag_id': falcon.tag_id,
            'espece': 'Non renseignée',
            'couleur': couleurs[i % len(couleurs)]
        })

    return render_template("birds.html",
        sous_titre="Fiches oiseaux",
        birds=oiseaux,
        form=form)


# Renvoie les codes de faucons pour précharger la recherche de la carte
@app.route("/recherche/base")
def recherche_base():
    falcons = Falcon.query.order_by(Falcon.falcon_code).all()
    return {
        f.falcon_code: f.falcon_code
        for f in falcons
    }