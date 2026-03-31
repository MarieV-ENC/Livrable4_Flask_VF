# 🦅 Migration animale 🦅

Le projet VOIE DE CRÉCERELLE cherche à déterminer et à mettre en valeur l’impact de l’activité humaine sur la migration d’un groupe de faucons crécerelles (Falco tinnunculus) en croisant des données animalières, géographiques et météorologiques.

Entre 2021 et 2023, la station biologique du parc national de Doñana (EDB) en Andalousie, en collaboration avec le Conseil supérieur de la recherche scientifique (CSIC), a équipé un échantillon de faucons crécerelles de balises GPS afin d’étudier leurs déplacements. Ce jeu de données sera croisé avec les relevés météorologiques issus de l'Agence d'État de météorologie espagnole (AEMET) ainsi qu’avec des données géographiques de Wikidata (espaces urbains, densité de population, reliefs…).

La base de données sera accessible via une interface web. Les données seront présentées sous la forme de données structurées et de datavisualisation afin de sensibiliser sur l’impact de l’homme sur l'éthologie de ces rapaces.

# L'équipe 👩🏻‍💻✍🏻💡

L'application a été créée par :
- Marie Vielmas
- Clara Martin
- Fanny Suszko
- Aristide Curtelin

# Deadlines du projet 📓

|Date              | Livrable        | Type de rendu         |
|------------------|-----------------|-----------------------|
| 15/02/2026       | Livrable n°3    | traitement de données |
| 01/03/2026       | Livrable n°4    | datavisualisation et journal de bord |
| 31/03/2026       | Livrable n°5    | application python    |

# Premiers pas avec l'application Flask

## Installer l'application en local

## 1. Cloner le dépôt

```bash
git clone git@github.com:MarieV-ENC/Livrable4_Flask_VF.git
cd Livrable4_Flask_VF.git
```

---

## 2. Paramétrer la base de donnée crec

Réalisez la procédure décrite dans le README.md du Livrable_3_Traitements_donnees afin de générer la base de donnée 'crec' sur laquelle s'appuient les fonctionnalités de l'application.

Résumé pour une exécution rapide :

```crec
cd Livrable_3_Traitements_donnees
python -m venv env
source env/Scripts/activate
pip install -r requirements.txt
python run.py
```
Veillez à copier le fichier `.env.example` en `.env`, puis adapter les valeurs à votre configuration locale (en particulier le mot de passe de votre session postgres)

Le script python run.py :

- crée la base si nécessaire,
- importe les CSV,
- exécute les scripts SQL automatiquement dans l’ordre alphabétique.

## 2. Paramétrer l'application Flask

1. Créer un environnement virtuel

```bash
cd Livrable4_Flask_VF
python3 -m venv env
source env/bin/activate
```
---

3. Installer les dépendances de l'application

```bash
pip install -r requirements.txt
```
---
4. Visualiser la carte interactive en javascript

Télécharger et installer Node.js (version LTS) à l'adresse https://nodejs.org/fr/download et télécharger la version LTS

```node
# Télécharger et installer nvm :
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash

# au lieu de redémarrer le shell
\. "$HOME/.nvm/nvm.sh"

# Télécharger et installer Node.js :
nvm install 24

# Vérifiez la version de Node.js :
node -v # Doit afficher "v24.14.1".

# Vérifier la version de npm :
npm -v # Doit afficher "11.11.0".
```

Vérifier l'installation

```
node --version
npm --version
```

Initialiser npm dans le projet (veiller à être dans le dossier du projet)

```
npm init -y
```
Installer Leaflet

```
npm install leaflet
```

Les fichiers Leaflet leaflet.css, leaflet.js et les images associées contenues dans node_modules/leaflet/dist doivent être placés dans le dossier static de l'application (dans ce git ces fichiers sont dors et déjà au bon emplacement).

5. Générrer le fichier GeoJSON

La carte interactive utilise certaines données sur les faucons contenues dans le fichier donnees.csv, données converties au format json (fichier data_js.json) par le script csv_to_geojson.py.

Pour obtenir le fichier data_js.json par l'exécution du script csv_to_geojson.py :

```script csv to json
python csv_to_geojson.py
```
Dans ce dépôt git le fichier data_js.json est déjà prêt à l'emploi.

Note : les donnees ont dans un premier temps été converties du format csv au format json afin de permettre la gestion automatique des points de géolocation (latitude, longitude) par les fonctionnalités de leaflet. En raison du volume des données, il n'est volontairement pris en compte qu'un 1 passage sur 1000 afin de favoriser une meilleure lisibilité de la carte dynamique. Certains paramètres de filtres ont été reliés dans un second temps directement aux données contenues dans la BDD crec.

6. Configurer les variables d’environnement pour relier l'app à la BDD crec

Transformer le fichier envexample en fichier .env à la racine du projet (ne pas oublier de préciser son mot de passe) :

```env
DEBUG=True

DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=crec

SECRET_KEY=dev
```
---

**crec**

Les tables principales de la BDD crec utilisées pour le projet sont :

- `crec.falcon`
- `crec.bird_detection`
- `crec.place`
- `crec.weather_station`
- `crec.weather_measurement`
- `crec.user_account`
- `crec.comment`

Si nécessaire, créer les tables utilisateurs et commentaires :

```sql
CREATE TABLE crec.user_account (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    bio TEXT
);
```

```sql
CREATE TABLE crec.comment (
    comment_id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL REFERENCES crec.user_account(user_id),
    falcon_id INTEGER NOT NULL REFERENCES crec.falcon(falcon_id)
);
```

---

7. Lancer le serveur Flask


```bash
python3 run.py
```

Le serveur sera accessible à l’adresse :

http://127.0.0.1:5000

---

8. Arrêter le serveur

Dans le terminal : Ctrl + C
