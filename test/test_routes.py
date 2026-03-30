import pytest

# ================================================================
# TESTS DES PAGES PUBLIQUES
# ================================================================

def test_page_accueil(client):
    """La page d'accueil répond correctement"""
    rv = client.get('/')
    assert rv.status_code == 200

def test_page_map(client):
    """La page carte répond correctement"""
    rv = client.get('/map')
    assert rv.status_code == 200

def test_page_birds(client):
    """La page fiches oiseaux répond correctement"""
    rv = client.get('/birds')
    assert rv.status_code == 200

def test_page_birds_contient_faucons(client):
    """La page fiches oiseaux contient bien des faucons"""
    rv = client.get('/birds')
    assert rv.status_code == 200
    # la page doit contenir au moins un code faucon
    assert b'falcon' in rv.data.lower() or b'faucon' in rv.data.lower()

def test_page_methodology(client):
    """La page méthodologie répond correctement"""
    rv = client.get('/methodology')
    assert rv.status_code == 200

def test_page_legal(client):
    """La page mentions légales répond correctement"""
    rv = client.get('/legal')
    assert rv.status_code == 200

def test_page_dataviz(client):
    """La page dataviz répond correctement"""
    rv = client.get('/dataviz')
    assert rv.status_code == 200

def test_page_404(client):
    """Une URL inexistante retourne bien un 404"""
    rv = client.get('/page-qui-nexiste-pas')
    assert rv.status_code == 404

def test_page_falcon_liste(client):
    """La route /falcon retourne la liste des faucons"""
    rv = client.get('/falcon')
    assert rv.status_code == 200

def test_recherche_base_json(client):
    """La route /recherche/base retourne bien un dictionnaire"""
    rv = client.get('/recherche/base')
    assert rv.status_code == 200


# ================================================================
# TESTS DES PAGES D'AUTHENTIFICATION
# ================================================================

def test_page_login_accessible(client):
    """La page de connexion s'affiche"""
    rv = client.get('/login')
    assert rv.status_code == 200

def test_page_login_contient_formulaire(client):
    """La page de connexion contient un formulaire"""
    rv = client.get('/login')
    assert b'form' in rv.data.lower()
    assert b'password' in rv.data.lower()

def test_page_register_accessible(client):
    """La page d'inscription s'affiche"""
    rv = client.get('/register')
    assert rv.status_code == 200

def test_page_register_contient_formulaire(client):
    """La page d'inscription contient un formulaire"""
    rv = client.get('/register')
    assert b'form' in rv.data.lower()
    assert b'username' in rv.data.lower() or b'identifiant' in rv.data.lower()

def test_login_mauvais_identifiants(client):
    """Un login avec de mauvais identifiants affiche une erreur"""
    rv = client.post('/login', data={
        'login': 'utilisateur_inexistant',
        'password': 'mauvais_mot_de_passe'
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert 'Identifiants incorrects.' in rv.data.decode('utf-8')

def test_login_champ_vide(client):
    """Un login avec des champs vides échoue"""
    rv = client.post('/login', data={
        'login': '',
        'password': ''
    }, follow_redirects=True)
    assert rv.status_code == 200
    # ne doit pas rediriger vers le profil
    assert 'Connexion réussie.' not in rv.data.decode('utf-8')


# ================================================================
# TESTS DES PAGES PROTÉGÉES (sans connexion)
# ================================================================

def test_profile_non_connecte_redirige(client):
    """Le profil est inaccessible sans connexion et redirige"""
    rv = client.get('/profile', follow_redirects=True)
    assert rv.status_code == 200
    # doit rediriger vers login
    assert 'login' in rv.request.path or b'connexion' in rv.data.lower() or b'login' in rv.data.lower()

def test_logout_non_connecte_redirige(client):
    """Le logout sans connexion redirige vers login"""
    rv = client.get('/logout', follow_redirects=True)
    assert rv.status_code == 200


# ================================================================
# TESTS DE L'INSCRIPTION
# ================================================================

def test_register_mots_de_passe_differents(client):
    """L'inscription échoue si les mots de passe ne correspondent pas"""
    rv = client.post('/register', data={
        'username': 'nouvel_user',
        'email': 'nouveau@test.com',
        'password': 'motdepasse123',
        'confirm_password': 'motdepassedifferent',
        'bio': ''
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert 'Les mots de passe ne correspondent pas.' in rv.data.decode('utf-8')

def test_register_username_existant(client, app_ctx):
    """L'inscription échoue si le nom d'utilisateur existe déjà"""
    from app.app import db
    from app.models.users import User

    # on crée d'abord un user en BDD de test
    user = User(username='user_existant', email='existant@test.com', bio='')
    user.set_password('motdepasse123')
    db.session.add(user)
    db.session.commit()

    rv = client.post('/register', data={
        'username': 'user_existant',
        'email': 'autre@test.com',
        'password': 'motdepasse123',
        'confirm_password': 'motdepasse123',
        'bio': ''
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert 'Cet identifiant existe déjà.' in rv.data.decode('utf-8')

    # nettoyage
    db.session.delete(user)
    db.session.commit()

def test_register_email_existant(client, app_ctx):
    """L'inscription échoue si l'email existe déjà"""
    from app.app import db
    from app.models.users import User

    user = User(username='user_email', email='dejaexistant@test.com', bio='')
    user.set_password('motdepasse123')
    db.session.add(user)
    db.session.commit()

    rv = client.post('/register', data={
        'username': 'autre_user',
        'email': 'dejaexistant@test.com',
        'password': 'motdepasse123',
        'confirm_password': 'motdepasse123',
        'bio': ''
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert 'Cette adresse mail existe déjà.' in rv.data.decode('utf-8')

    # nettoyage
    db.session.delete(user)
    db.session.commit()


# ================================================================
# TESTS DES FICHES OISEAUX
# ================================================================

def test_fiche_oiseau_existant(client):
    """La fiche d'un faucon existant s'affiche"""
    rv = client.get('/bird/BA8912')
    assert rv.status_code == 200

def test_fiche_oiseau_existant_contient_code(client):
    """La fiche d'un faucon affiche son code"""
    rv = client.get('/bird/BA8912')
    assert rv.status_code == 200
    assert b'BA8912' in rv.data

def test_fiche_oiseau_inexistant(client):
    """La fiche d'un faucon inexistant s'affiche sans erreur serveur"""
    rv = client.get('/bird/FAUCON_INEXISTANT_XYZ')
    assert rv.status_code == 200

def test_commentaire_non_connecte(client):
    """Un utilisateur non connecté ne peut pas poster de commentaire"""
    rv = client.post('/bird/BA8912', data={
        'comment': 'Test commentaire'
    }, follow_redirects=True)
    # la page doit s'afficher sans erreur serveur
    assert rv.status_code == 200


# ================================================================
# TESTS DE LA RECHERCHE
# ================================================================

def test_page_search_accessible(client):
    """La page de recherche s'affiche"""
    rv = client.get('/search')
    assert rv.status_code == 200

def test_page_search_contient_formulaire(client):
    """La page de recherche contient un formulaire"""
    rv = client.get('/search')
    assert b'form' in rv.data.lower()

def test_recherche_sans_filtre(client):
    """La page /recherche sans filtre s'affiche sans erreur"""
    rv = client.get('/recherche')
    assert rv.status_code == 200

def test_recherche_avec_code_faucon(client):
    """La recherche filtrée par code faucon fonctionne"""
    rv = client.get('/recherche?code_faucon=BA8912')
    assert rv.status_code == 200

def test_recherche_avec_date(client):
    """La recherche filtrée par date fonctionne"""
    rv = client.get('/recherche?date_filtre=2024-01-01')
    assert rv.status_code == 200

def test_recherche_avec_place(client):
    """La recherche filtrée par lieu fonctionne"""
    rv = client.get('/recherche?place=Madrid')
    assert rv.status_code == 200

def test_recherche_date_invalide(client):
    """Une date invalide ne provoque pas d'erreur serveur"""
    rv = client.get('/recherche?date_filtre=date-invalide')
    assert rv.status_code == 200

def test_recherche_page_2(client):
    """La pagination fonctionne"""
    rv = client.get('/recherche/2?code_faucon=BA8912')
    assert rv.status_code == 200
