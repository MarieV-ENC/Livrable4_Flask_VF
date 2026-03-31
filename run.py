# Importer l'application Flask principale
from app.app import app

# Lancer l'application uniquement si ce fichier est exécuté directement
if __name__ == "__main__":

    # Démarrer le serveur Flask
    # Le mode debug dépend de la configuration définie dans l'application
    app.run(debug=app.config["DEBUG"])