import pytest
from app.models.crec import Falcon, Bird_detection, Place, Weather_station, Weather_measurement
from app.models.users import User
from app.models.comment import Comment
from app.app import db


# ================================================================
# TESTS DU MODÈLE FALCON
# ================================================================

def test_falcon_table_accessible(app_ctx):
    """La table Falcon est accessible"""
    falcons = Falcon.query.all()
    assert isinstance(falcons, list)

def test_falcon_table_non_vide(app_ctx):
    """La table Falcon contient des données"""
    falcons = Falcon.query.all()
    assert len(falcons) > 0

def test_falcon_code_existant(app_ctx):
    """Le faucon BA8912 existe en BDD"""
    falcon = Falcon.query.filter_by(falcon_code='BA8912').first()
    assert falcon is not None
    assert falcon.falcon_code == 'BA8912'

def test_falcon_champs_presents(app_ctx):
    """Un faucon possède bien les champs attendus"""
    falcon = Falcon.query.first()
    assert hasattr(falcon, 'falcon_id')
    assert hasattr(falcon, 'falcon_code')
    assert hasattr(falcon, 'tag_id')
    assert hasattr(falcon, 'nickname')

def test_falcon_code_unique(app_ctx):
    """Deux faucons ne peuvent pas avoir le même code"""
    falcons = Falcon.query.all()
    codes = [f.falcon_code for f in falcons]
    assert len(codes) == len(set(codes))

def test_falcon_relation_detections(app_ctx):
    """Un faucon a une relation vers ses détections"""
    falcon = Falcon.query.first()
    assert hasattr(falcon, 'detections')

def test_falcon_relation_comments(app_ctx):
    """Un faucon a une relation vers ses commentaires"""
    falcon = Falcon.query.first()
    assert hasattr(falcon, 'comments')


# ================================================================
# TESTS DU MODÈLE BIRD_DETECTION
# ================================================================

def test_bird_detection_accessible(app_ctx):
    """La table Bird_detection est accessible"""
    detections = Bird_detection.query.limit(10).all()
    assert isinstance(detections, list)

def test_bird_detection_champs_presents(app_ctx):
    """Une détection possède bien les champs attendus"""
    detection = Bird_detection.query.first()
    if detection:
        assert hasattr(detection, 'detection_id')
        assert hasattr(detection, 'time')
        assert hasattr(detection, 'falcon_id')
        assert hasattr(detection, 'place_id')


# ================================================================
# TESTS DU MODÈLE PLACE
# ================================================================

def test_place_accessible(app_ctx):
    """La table Place est accessible"""
    places = Place.query.limit(10).all()
    assert isinstance(places, list)

def test_place_champs_presents(app_ctx):
    """Un lieu possède bien les champs attendus"""
    place = Place.query.first()
    if place:
        assert hasattr(place, 'place_id')
        assert hasattr(place, 'space_label')
        assert hasattr(place, 'place_lat')
        assert hasattr(place, 'place_lon')


# ================================================================
# TESTS DU MODÈLE USER
# ================================================================

def test_user_creation_basique(app_ctx):
    """Un utilisateur peut être créé avec les bons champs"""
    user = User(
        username='test_user_pytest',
        email='pytest@test.com',
        bio='bio de test'
    )
    user.set_password('motdepasse123')
    assert user.username == 'test_user_pytest'
    assert user.email == 'pytest@test.com'

def test_user_mot_de_passe_correct(app_ctx):
    """Le bon mot de passe est accepté"""
    user = User(username='u1', email='u1@test.com', bio='')
    user.set_password('motdepasse123')
    assert user.check_password('motdepasse123') == True

def test_user_mauvais_mot_de_passe(app_ctx):
    """Un mauvais mot de passe est refusé"""
    user = User(username='u2', email='u2@test.com', bio='')
    user.set_password('motdepasse123')
    assert user.check_password('mauvais_mdp') == False

def test_user_get_id(app_ctx):
    """get_id retourne bien une chaîne"""
    user = User(username='u3', email='u3@test.com', bio='')
    user.user_id = 42
    assert user.get_id() == '42'

def test_user_mot_de_passe_hache(app_ctx):
    """Le mot de passe est bien haché et non stocké en clair"""
    user = User(username='u4', email='u4@test.com', bio='')
    user.set_password('motdepasse123')
    assert user.password_hash != 'motdepasse123'
    assert len(user.password_hash) > 20

def test_user_persistance_bdd(app_ctx):
    """Un utilisateur peut être sauvegardé et récupéré en BDD"""
    user = User(
        username='user_test_persist',
        email='persist@test.com',
        bio='test'
    )
    user.set_password('motdepasse123')
    db.session.add(user)
    db.session.commit()

    recupere = User.query.filter_by(username='user_test_persist').first()
    assert recupere is not None
    assert recupere.email == 'persist@test.com'

    # nettoyage
    db.session.delete(recupere)
    db.session.commit()

def test_user_relation_comments(app_ctx):
    """Un utilisateur a une relation vers ses commentaires"""
    user = User(username='u5', email='u5@test.com', bio='')
    assert hasattr(user, 'comments')


# ================================================================
# TESTS DU MODÈLE COMMENT
# ================================================================

def test_comment_table_accessible(app_ctx):
    """La table Comment est accessible"""
    comments = Comment.query.limit(10).all()
    assert isinstance(comments, list)

def test_comment_creation(app_ctx):
    """Un commentaire peut être créé et sauvegardé"""
    # on crée un user et un falcon de test
    user = User(username='user_comment', email='comment@test.com', bio='')
    user.set_password('motdepasse123')
    db.session.add(user)
    db.session.flush()  # pour obtenir user_id sans commit

    falcon = Falcon.query.first()
    assert falcon is not None

    from datetime import datetime
    comment = Comment(
        content='Commentaire de test pytest',
        user_id=user.user_id,
        falcon_id=falcon.falcon_id
    )
    db.session.add(comment)
    db.session.commit()

    recupere = Comment.query.filter_by(content='Commentaire de test pytest').first()
    assert recupere is not None
    assert recupere.content == 'Commentaire de test pytest'

    # nettoyage
    db.session.delete(recupere)
    db.session.delete(user)
    db.session.commit()

def test_comment_champs_presents(app_ctx):
    """Un commentaire possède bien les champs attendus"""
    comment = Comment(content='test', user_id=1, falcon_id=1)
    assert hasattr(comment, 'comment_id')
    assert hasattr(comment, 'content')
    assert hasattr(comment, 'created_at')
    assert hasattr(comment, 'user_id')
    assert hasattr(comment, 'falcon_id')


# ================================================================
# TESTS DU MODÈLE WEATHER
# ================================================================

def test_weather_station_accessible(app_ctx):
    """La table Weather_station est accessible"""
    stations = Weather_station.query.limit(5).all()
    assert isinstance(stations, list)

def test_weather_measurement_accessible(app_ctx):
    """La table Weather_measurement est accessible"""
    mesures = Weather_measurement.query.limit(5).all()
    assert isinstance(mesures, list)
