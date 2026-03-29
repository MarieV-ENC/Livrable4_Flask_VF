from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models.crec import Falcon, Bird_detection, Place, Weather_station, Weather_measurement
from ..models.comment import Comment
from ..models.users import User
from ..app import app, db
from sqlalchemy import or_, text
from flask import current_app
from ..models.formulaires import Recherche
from ..config import clean_arg
from ..models.formulaires import Recherche, Modification
from datetime import datetime
from datetime import datetime, timedelta
import os
import json
import csv

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/map")
def map_page():
    return render_template("map.html")


@app.route("/search")
def search():
    formulaire_oiseau = Recherche ()
    surnoms_path = os.path.join(app.static_folder, 'data', 'surnoms.json')
    with open(surnoms_path, 'r', encoding='utf-8') as f:
        surnoms = json.load(f)

    formulaire_oiseau.code_faucon.choices = [('', '-- Tous --')] + [
        (code, surnom) for code, surnom in surnoms.items()
    ]
    return render_template("search.html", form=formulaire_oiseau) 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_value = request.form["login"]
        password = request.form["password"]

        user = User.query.filter(
            (User.username == login_value) | (User.email == login_value)
        ).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Connexion réussie.")
            return redirect(url_for("profile"))

        flash("Identifiants incorrects.")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        bio = request.form.get("bio", "").strip()

        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.")
            return redirect(url_for("register"))

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash("Cet identifiant existe déjà.")
            return redirect(url_for("register"))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("Cette adresse mail existe déjà.")
            return redirect(url_for("register"))

        user = User(
            username=username,
            email=email, 
            bio=bio
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Compte créé. Vous pouvez vous connecter.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.")
    return redirect(url_for("index"))

# modif de cette route pour avoir str 
@app.route("/bird/<falcon_id>", methods=["GET", "POST"])
def bird_detail(falcon_id):
    import csv
    import json
    import os

    # Charger les surnoms
    surnoms_path = os.path.join(app.static_folder, 'data', 'surnoms.json')
    with open(surnoms_path, 'r', encoding='utf-8') as f:
        surnoms = json.load(f)

    # Récupérer les infos de l'oiseau depuis le CSV
    bird = None
    with open('donnees.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['individual-local-identifier'] == falcon_id:
                bird = {
                    'falcon_id': falcon_id,
                    'falcon_code': falcon_id,
                    'nickname': surnoms.get(falcon_id, 'NONE'),
                    'tag_id': row.get('tag-local-identifier', None),
                    'espece': row.get('individual-taxon-canonical-name', 'Non renseignée')
                }
                break  # on s'arrête dès qu'on a trouvé l'oiseau

    return render_template("bird_detail.html", bird=bird, comments=[])




@app.route("/bird")
def bird_detail_first():
    falcon = Falcon.query.first()

    return render_template(
        "bird_detail.html",
        bird=falcon,
        comments=[]
    )



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


@app.route("/methodology")
def methodology():
    return render_template("methodology.html")


@app.route("/dataviz")
def dataviz():
    return render_template("dataviz.html")





@app.route("/legal")
def legal():
    return render_template("legal.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.route("/falcon")
def list_falcon():
    from ..models.crec import Falcon

    donnees = []

    for f in Falcon.query.all():
        donnees.append({
            "falcon_code": f.falcon_code,
            "tag_id": f.tag_id,
            "nickname": f.nickname
        })

    return render_template(
        "falcon_test.html",  
        donnees=donnees,
        sous_titre="tous nos pigeons"
    )

@app.route("/recherche", methods=['GET'])
@app.route("/recherche/<int:page>", methods=['GET'])
def recherche(page=1):
    form = Recherche()

    # Chargement dynamique des choix depuis surnoms.json
    surnoms_path = os.path.join(app.static_folder, 'data', 'surnoms.json')
    with open(surnoms_path, 'r', encoding='utf-8') as f:
        surnoms = json.load(f)

    form.code_faucon.choices = [('', '-- Tous --')] + [
        (code, surnom) for code, surnom in surnoms.items()
    ]

    code_faucon = clean_arg(request.args.get("code_faucon", None))
    date_filtre = clean_arg(request.args.get("date", None))
    place_filtre = clean_arg(request.args.get("place", None))

    # date_obj défini AVANT form.date_filtre.data
    date_obj = None
    if date_filtre:
        try:
            date_obj = datetime.strptime(date_filtre, "%Y-%m-%d").date()
        except ValueError:
            pass

    form.code_faucon.data = code_faucon
    form.date_filtre.data = date_obj
    form.place.data = place_filtre

    donnees = []

    if code_faucon or date_obj or place_filtre:
        query_results = db.session.query(Bird_detection)

        if code_faucon:
            query_results = query_results.join(
                Falcon, Falcon.falcon_id == Bird_detection.falcon_id
            ).filter(
                Falcon.falcon_code.ilike("%" + code_faucon.lower() + "%")
            )

        if date_obj:
            from datetime import time
            debut = datetime.combine(date_obj, time(0, 0, 0))
            fin = datetime.combine(date_obj + timedelta(days=1), time(0, 0, 0))
            query_results = query_results.filter(
                Bird_detection.time >= debut,
                Bird_detection.time < fin
            )

        if place_filtre:
            query_results = query_results.join(
                Place, Place.place_id == Bird_detection.place_id
            ).filter(
                Place.space_label.ilike("%" + place_filtre.lower() + "%")
            )

        donnees = query_results \
            .order_by(Bird_detection.time) \
            .paginate(page=page, per_page=app.config["DETECTIONS_PER_PAGE"])

    return render_template("search.html",
            sous_titre="Recherche",
            donnees=donnees,
            form=form)

@app.route("/birds", methods=['GET', 'POST'])
def birds():
    form = Modification()

    surnoms_path = os.path.join(app.static_folder, 'data', 'surnoms.json')
    with open(surnoms_path, 'r', encoding='utf-8') as f:
        surnoms = json.load(f)

    form.code_faucon.choices = [('', '-- Tous --')] + [
        (code, surnom) for code, surnom in surnoms.items()
    ]

    if form.validate_on_submit():
        code_faucon = clean_arg(request.form.get("code_faucon", None))
        nom_faucon = clean_arg(request.form.get("nom_faucon", None))

        surnoms[code_faucon] = nom_faucon

        with open(surnoms_path, 'w', encoding='utf-8') as f:
            json.dump(surnoms, f, ensure_ascii=False, indent=2)

        flash(f"Surnom « {nom_faucon} » enregistré avec succès.")
        return redirect(url_for("birds"))

    # GET — chargement des oiseaux
    couleurs = [
        '#e41a1c', '#377eb8', '#4daf4a', '#984ea3',
        '#ff7f00', '#a65628', '#f781bf', '#999999',
        '#17becf', '#bcbd22', '#ff9896', '#aec7e8'
    ]

    oiseaux = []
    seen = set()

    with open('donnees.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            identifiant = row['individual-local-identifier']
            if identifiant not in seen:
                seen.add(identifiant)
                oiseaux.append({
                    'falcon_id': identifiant,
                    'falcon_code': identifiant,
                    'nickname': surnoms.get(identifiant, 'NONE'),
                    'tag_id': row.get('tag-local-identifier', None),
                    'espece': row.get('individual-taxon-canonical-name', 'Non renseignée'),
                    'couleur': couleurs[len(oiseaux) % len(couleurs)]
                })

    return render_template("birds.html",
        sous_titre="Fiches oiseaux",
        birds=oiseaux,
        form=form)


        