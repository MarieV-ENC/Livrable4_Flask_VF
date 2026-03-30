# Mapping de la BDD
from ..app import db

# Bird detection

class Bird_detection (db.Model):
    __tablename__ = "bird_detection"
    __table_args__ = {"schema": "crec"}

    detection_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False
    )

    time = db.Column(
        db.DateTime,
    )

    coordinate = db.Column(
        db.Float,
    )

    speed = db.Column(
        db.Float,
    )

    altitude = db.Column(
        db.Float,
    )

    falcon_id = db.Column(
        db.Integer,
        db.ForeignKey("crec.falcon.falcon_id"),
        nullable=False
        
    )

    place_id = db.Column(
        db.Integer,
        db.ForeignKey("crec.place.place_id"),
    )

    # propriété de relation avec falcon

    DetectionsFalcon = db.relationship(
        "Falcon",
        backref="detections",
        lazy=True
    )

    # propriété de relation avec place

    DetectionsPlace = db.relationship(
        "Place",
        backref="passage",
        lazy=True
    )

# falcon

class Falcon(db.Model):
    __tablename__ = "falcon"
    __table_args__ = {"schema": "crec"}

    falcon_id = db.Column(
        db.Integer,
        primary_key=True
    )

    falcon_code = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )

    tag_id = db.Column(
        db.Text
    )

    nickname = db.Column(
        db.Text,
        nullable=False
    )

    # relation vers les commentaires
    comments = db.relationship(
        "Comment",
        backref="falcon",
        lazy=True
    )

# Place


class Place(db.Model):
    __tablename__ = "place"
    __table_args__ = {"schema": "crec"}

    place_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False
    )

    space_label = db.Column(
        db.Text,
    )

    wikidata_id = db.Column(
        db.Text
    )

    type_label = db.Column(
        db.Text
    )

    ccaa_label = db.Column(
        db.Text
    )

    province_label = db.Column(
        db.Text
    )

    coordonnees = db.Column(
        db.Text
    )

    elevation = db.Column(
        db.Float
    )

    area = db.Column(
        db.Float
    )

    population = db.Column(
        db.Integer
    )

    place_lat = db.Column(
        db.Float
    )

    place_lon = db.Column(
        db.Float
    )


    province_key = db.Column(
        db.Text
    )

    ccaa_key = db.Column(
        db.Text
    )

    province_std = db.Column(
        db.Text
    )

    ccaa_std = db.Column(
        db.Text
    )

# weather_measurement 

class Weather_measurement(db.Model):
    __tablename__ = "weather_measurement"
    __table_args__ = {"schema": "crec"}

    measurement_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False
    )

    obs_date = db.Column(
        db.Date,
        nullable=False
    )

    time = db.Column(
        db.DateTime,
        nullable=False
    )

    temperature_min = db.Column(
        db.Float
    )

    temperature_mid = db.Column(
        db.Float
    )

    temperature_max = db.Column(
        db.Float
    )

    humidity_min = db.Column(
        db.Float
    )

    humidity_mid = db.Column(
        db.Float
    )

    humidity_max = db.Column(
        db.Float
    )

    precip = db.Column(
        db.Float
    )

    wind_speed_mid = db.Column(
        db.Float
    )

    wind_gust = db.Column(
        db.Float
    )

    wind_direction = db.Column(
        db.Float
    )

    station_id = db.Column(
        db.Integer,
        db.ForeignKey("crec.weather_station.station_id"),
        nullable=False
    )

# propriété de relation avec weather_station

    StationMeasure = db.relationship(
        "Weather_station",
        backref="measure",
        lazy=True
    )

# weather_station

class Weather_station(db.Model):
    __tablename__ = "weather_station"
    __table_args__ = {"schema": "crec"}

    station_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False
    )

    station_code = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.Text,
        nullable=False
    )

    province = db.Column(
        db.Text
    )

    place_id = db.Column(
        db.Integer,
        db.ForeignKey("crec.place.place_id")
    )

# propriété de relation avec place

    Repartition = db.relationship(
        "Place",
        backref="observations",
        lazy=True
    )