# Import de l'objet db permettant de définir les tables et relations SQLAlchemy
from ..app import db


# =========================
# Table des détections d'oiseaux
# =========================
class Bird_detection(db.Model):
    # Nom de la table et schéma associé
    __tablename__ = "bird_detection"
    __table_args__ = {"schema": "crec"}

    # Identifiant unique d'une détection
    detection_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False
    )

    # Date et heure de la détection
    time = db.Column(
        db.DateTime,
    )

    # Coordonnée enregistrée lors de la détection
    coordinate = db.Column(
        db.Float,
    )

    # Vitesse du faucon au moment de la détection
    speed = db.Column(
        db.Float,
    )

    # Altitude du faucon au moment de la détection
    altitude = db.Column(
        db.Float,
    )

    # Clé étrangère vers le faucon détecté
    falcon_id = db.Column(
        db.Integer,
        db.ForeignKey("crec.falcon.falcon_id"),
        nullable=False
    )

    # Clé étrangère vers le lieu de la détection
    place_id = db.Column(
        db.Integer,
        db.ForeignKey("crec.place.place_id"),
    )

    # Relation entre une détection et un faucon
    DetectionsFalcon = db.relationship(
        "Falcon",
        backref="detections",
        lazy=True
    )

    # Relation entre une détection et un lieu
    DetectionsPlace = db.relationship(
        "Place",
        backref="passage",
        lazy=True
    )


# =========================
# Table des faucons
# =========================
class Falcon(db.Model):
    __tablename__ = "falcon"
    __table_args__ = {"schema": "crec"}

    # Identifiant unique du faucon
    falcon_id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Code unique du faucon dans la base
    falcon_code = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )

    # Identifiant de la balise GPS
    tag_id = db.Column(
        db.Text
    )

    # Nom ou surnom donné au faucon
    nickname = db.Column(
        db.Text,
        nullable=False
    )

    # Relation entre un faucon et ses commentaires
    comments = db.relationship(
        "Comment",
        backref="falcon",
        lazy=True
    )


# =========================
# Table des lieux
# =========================
class Place(db.Model):
    __tablename__ = "place"
    __table_args__ = {"schema": "crec"}

    # Identifiant unique du lieu
    place_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False
    )

    # Nom du lieu
    space_label = db.Column(
        db.Text,
    )

    # Identifiant Wikidata du lieu
    wikidata_id = db.Column(
        db.Text
    )

    # Type du lieu (ville, région, etc.)
    type_label = db.Column(
        db.Text
    )

    # Communauté autonome associée
    ccaa_label = db.Column(
        db.Text
    )

    # Province associée
    province_label = db.Column(
        db.Text
    )

    # Coordonnées du lieu sous forme de texte
    coordonnees = db.Column(
        db.Text
    )

    # Altitude du lieu
    elevation = db.Column(
        db.Float
    )

    # Surface du lieu
    area = db.Column(
        db.Float
    )

    # Population du lieu
    population = db.Column(
        db.Integer
    )

    # Latitude du lieu
    place_lat = db.Column(
        db.Float
    )

    # Longitude du lieu
    place_lon = db.Column(
        db.Float
    )

    # Version normalisée du nom de province
    province_key = db.Column(
        db.Text
    )

    # Version normalisée du nom de communauté autonome
    ccaa_key = db.Column(
        db.Text
    )

    # Province standardisée
    province_std = db.Column(
        db.Text
    )

    # Communauté autonome standardisée
    ccaa_std = db.Column(
        db.Text
    )


# =========================
# Table des mesures météo
# =========================
class Weather_measurement(db.Model):
    __tablename__ = "weather_measurement"
    __table_args__ = {"schema": "crec"}

    # Identifiant unique de la mesure météo
    measurement_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False
    )

    # Date de l'observation
    obs_date = db.Column(
        db.Date,
        nullable=False
    )

    # Date et heure précises de la mesure
    time = db.Column(
        db.DateTime,
        nullable=False
    )

    # Températures minimale, moyenne et maximale
    temperature_min = db.Column(db.Float)
    temperature_mid = db.Column(db.Float)
    temperature_max = db.Column(db.Float)

    # Humidités minimale, moyenne et maximale
    humidity_min = db.Column(db.Float)
    humidity_mid = db.Column(db.Float)
    humidity_max = db.Column(db.Float)

    # Quantité de précipitations
    precip = db.Column(
        db.Float
    )

    # Vent moyen, rafales et direction
    wind_speed_mid = db.Column(db.Float)
    wind_gust = db.Column(db.Float)
    wind_direction = db.Column(db.Float)

    # Clé étrangère vers la station météo
    station_id = db.Column(
        db.Integer,
        db.ForeignKey("crec.weather_station.station_id"),
        nullable=False
    )

    # Relation entre une mesure et sa station météo
    StationMeasure = db.relationship(
        "Weather_station",
        backref="measure",
        lazy=True
    )


# =========================
# Table des stations météo
# =========================
class Weather_station(db.Model):
    __tablename__ = "weather_station"
    __table_args__ = {"schema": "crec"}

    # Identifiant unique de la station
    station_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False
    )

    # Code unique de la station météo
    station_code = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )

    # Nom de la station
    name = db.Column(
        db.Text,
        nullable=False
    )

    # Province dans laquelle se trouve la station
    province = db.Column(
        db.Text
    )

    # Clé étrangère vers le lieu associé à la station
    place_id = db.Column(
        db.Integer,
        db.ForeignKey("crec.place.place_id")
    )

    # Relation entre une station météo et un lieu
    Repartition = db.relationship(
        "Place",
        backref="observations",
        lazy=True
    )