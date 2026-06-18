# Importation des modules nécessaires
from flask import Flask, request, jsonify  # Flask pour créer l'API, request pour récupérer les paramètres de l'URL, jsonify pour renvoyer du JSON
import numpy as np                          # Numpy pour effectuer les calculs statistiques (moyenne, médiane, etc.)
from scipy import stats                     # Scipy pour calculer le coefficient de corrélation de Pearson et la p-value
from db import fetch_series                 # Importation de la fonction fetch_series depuis ton fichier db.py pour lire MySQL
from flask_cors import CORS
app = Flask(__name__)        # 2. Tu crées 'app' ICI
CORS(app)

# Initialisation de l'application Flask
app = Flask(__name__)

# ==============================================================================
# ROUTE 1 — Description des données depuis MySQL
# URL attendue : GET http://localhost:5003/db/stats/describe?serie=nom_de_la_serie
# ==============================================================================
@app.route('/db/stats/describe', methods=['GET'])
def db_describe():
    # 1. Récupération du paramètre 'serie' envoyé dans l'URL (ex: ?serie=serie_A)
    nom_serie = request.args.get('serie')
    
    # 2. Sécurité : Vérification que le paramètre a bien été fourni
    if not nom_serie:
        # Si le paramètre manque, on renvoie une erreur 400 (Bad Request)
        return jsonify({'erreur': "Paramètre 'serie' manquant"}), 400
        
    try:
        # 3. Récupération des données depuis MySQL via la fonction du fichier db.py
        # On convertit directement la liste reçue en un "Array" Numpy pour faciliter les calculs
        values = np.array(fetch_series(nom_serie))
        
        # 4. Calculs statistiques à l'aide de Numpy
        # On utilise float() et int() car les types natifs Numpy ne se convertissent pas bien en JSON.
        # round(..., 4) permet de limiter l'affichage à 4 chiffres après la virgule.
        result = {
            'serie': nom_serie,
            'n': int(len(values)),                                       # Nombre total d'éléments dans la série
            'moyenne': round(float(np.mean(values)), 4),                 # Calcul de la moyenne arithmétique
            'mediane': round(float(np.median(values)), 4),               # Calcul de la médiane (valeur centrale)
            'ecart_type': round(float(np.std(values, ddof=1)), 4),       # Écart-type d'échantillon (ddof=1 pour diviser par n-1)
            'minimum': round(float(np.min(values)), 4),                  # Valeur la plus basse
            'maximum': round(float(np.max(values)), 4),                  # Valeur la plus haute
        }
        
        # 5. Réponse : On renvoie le résultat au format JSON avec un code de succès (200 par défaut)
        return jsonify({'source': 'mysql', 'resultat': result})
        
    except ValueError as e:
        # Si fetch_series lève une erreur (ex: série introuvable), on renvoie une erreur 404 (Not Found)
        return jsonify({'erreur': str(e)}), 404
    except Exception as e:
        # Pour toute autre erreur (problème de connexion MySQL par exemple), on renvoie une erreur système 500
        return jsonify({'erreur': 'Erreur base de données', 'detail': str(e)}), 500


# ==============================================================================
# ROUTE 2 — Corrélation entre deux séries depuis MySQL
# URL attendue : GET http://localhost:5003/db/stats/correlation?serie_x=serie_A&serie_y=serie_B
# ==============================================================================
@app.route('/db/stats/correlation', methods=['GET'])
def db_correlation():
    # 1. Récupération des deux séries à comparer depuis l'URL
    serie_x = request.args.get('serie_x')
    serie_y = request.args.get('serie_y')
    
    # 2. Sécurité : Vérification que les deux paramètres sont présents
    if not serie_x or not serie_y:
        return jsonify({'erreur': 'Paramètres serie_x et serie_y requis'}), 400
        
    try:
        # 3. Récupération des données des deux séries depuis la base de données
        x = np.array(fetch_series(serie_x))
        y = np.array(fetch_series(serie_y))
        
        # 4. Alignement des données (Indispensable pour Pearson)
        # La corrélation nécessite que les deux listes aient exactement la même taille.
        # On cherche la taille minimale entre les deux séries.
        n = min(len(x), len(y))
        # On tronque les deux séries à cette taille commune 'n' pour aligner les points
        x, y = x[:n], y[:n]
        
        # 5. Calcul de la corrélation de Pearson à l'aide de Scipy
        # r = coefficient de corrélation (compris entre -1 et 1)
        # p_value = probabilité que la corrélation soit due au hasard
        r, p_value = stats.pearsonr(x, y)
        
        # 6. Structuration de la réponse JSON
        return jsonify({
            'source': 'mysql',
            'series': {'x': serie_x, 'y': serie_y, 'n_points': n},
            'resultat': {
                'r': round(float(r), 4),
                'p_value': round(float(p_value), 6),
                # Si la p-value est inférieure à 0.05 (5%), la corrélation est statistiquement significative
                'significatif': bool(p_value < 0.05)
            }
        })
        
    except ValueError as e:
        # Gestion de l'erreur si l'une des séries est introuvable ou vide
        return jsonify({'erreur': str(e)}), 404
    except Exception as e:
        # Gestion des autres erreurs (ex: crash SQL)
        return jsonify({'erreur': 'Erreur base de données', 'detail': str(e)}), 500


# Point d'entrée principal du script
if __name__ == '__main__':
    # Lancement du serveur de développement Flask
    # debug=True permet de recharger automatiquement le code dès que tu fais une modification
    # port=5003 est le port imposé par le sujet pour le Service 3
    app.run(debug=True, port=5003)