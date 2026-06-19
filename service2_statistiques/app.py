# Importation des modules nécessaires
from flask import Flask, request, jsonify  # Flask pour l'API, request pour intercepter le JSON reçu, jsonify pour sérialiser la réponse en JSON
import numpy as np                         # numpy pour les calculs mathématiques rapides (moyenne, médiane, écart-type...)
from scipy import stats                    # scipy.stats pour les calculs statistiques avancés (Pearson, Shapiro-Wilk)

# Initialisation de l'application Flask
app = Flask(__name__)

# Fonction utilitaire pour valider les données reçues (Robustesse du code)
def validate_data(data, key='data'):
    """Valide et retourne une liste de nombres sous forme de tableau numpy."""
    # 1. Vérification de la présence de la clé attendue (ex: 'data', 'x' ou 'y') dans l'objet JSON
    if key not in data:
        raise ValueError(f"Clé '{key}' manquante dans la requête")
    
    values = data[key]
    
    # 2. Vérification du type (doit être une liste) et de la taille (au moins 2 valeurs requises pour un calcul statistique)
    if not isinstance(values, list) or len(values) < 2:
        raise ValueError("'data' doit être une liste d'au moins 2 valeurs")
        
    # 3. Conversion de la liste brute en tableau numpy de type float pour sécuriser les calculs ultérieurs
    return np.array(values, dtype=float)

# =========================================================================
# Route 1 — Description statistique (Indicateurs clés d'une série)
# =========================================================================
@app.route('/stats/describe', methods=['POST'])
def describe():
    # Récupération du corps de la requête HTTP envoyé en JSON (le payload)
    data = request.get_json()
    try:
        # Validation de la série statistique fournie sous la clé par défaut 'data'
        values = validate_data(data)
        
        # Construction du dictionnaire de résultats en exploitant les fonctions vectorielles de NumPy
        result = {
            'n': int(len(values)),                                        # Taille de l'échantillon
            'moyenne': round(float(np.mean(values)), 4),                  # Moyenne arithmétique arrondie à 4 décimales
            'mediane': round(float(np.median(values)), 4),                # Médiane (valeur centrale partageant la série en deux)
            'ecart_type': round(float(np.std(values, ddof=1)), 4),        # Écart-type d'échantillon (dispersion autour de la moyenne, ddof=1 pour une division par N-1 afin de calculer la taille de l'echantillon)
            'variance': round(float(np.var(values, ddof=1)), 4),          # Variance d'échantillon (carré de l'écart-type, ddof=1 pour éviter le biais)
            'minimum': round(float(np.min(values)), 4),                    # Plus petite valeur de la série
            'maximum': round(float(np.max(values)), 4),                    # Plus grande valeur de la série
            'q1': round(float(np.percentile(values, 25)), 4),             # Premier quartile (25% des données sont inférieures ou égales)
            'q3': round(float(np.percentile(values, 75)), 4),             # Troisième quartile (75% des données sont inférieures ou égales)
            'etendue': round(float(np.ptp(values)), 4),                   # Étendue de la série (Maximum - Minimum)
        }
        # Retourne une réponse HTTP 200 OK avec la structure JSON attendue
        return jsonify({'operation': 'description', 'resultat': result})
    
    except (ValueError, TypeError) as e:
        # Intercepte les erreurs de format/type de données sans faire planter le serveur Flask
        # Retourne un code HTTP 400 Bad Request avec le message d'erreur explicite
        return jsonify({'erreur': str(e)}), 400


# =========================================================================
# Route 2 — Corrélation de Pearson (Lien linéaire entre deux séries)
# =========================================================================
@app.route('/stats/correlation', methods=['POST'])
def correlation():
    data = request.get_json()
    try:
        # On valide séparément la présence et la structure des deux séries distinctes 'x' et 'y'
        x_values = validate_data(data, key='x')
        y_values = validate_data(data, key='y')
        
        # Condition logique impérative : on ne peut corréler mathématiquement que des paires de données
        if len(x_values) != len(y_values):
            return jsonify({'erreur': 'Les listes x et y doivent avoir la même taille'}), 400
            
        # Calcul simultané du coefficient de Pearson (r) et de la p-value associée via scipy
        corr_coeff, p_value = stats.pearsonr(x_values, y_values)
        
        # Interprétation de la p-value : significative si inférieure au seuil universel de 0.05
        result = {
            'coefficient': round(float(corr_coeff), 4),                   # Force et direction de la relation (-1 à 1)
            'p_value': round(float(p_value), 4),                          # Probabilité d'observer ce résultat sous l'hypothèse nulle
            'interpretation': "Corrélation américaine significative" if p_value < 0.05 else "Corrélation non significative"
        }
        
        return jsonify({'operation': 'correlation', 'resultat': result})
        
    except (ValueError, TypeError) as e:
        # Gestion défensive des erreurs de saisie client (renvoie un code 400 au lieu de crasher en interne)
        return jsonify({'erreur': str(e)}), 400
    

# =========================================================================
# Route 3 — Test de normalité 
# =========================================================================
@app.route('/stats/test_normalite', methods=['POST'])
def test_normalite():
    data = request.get_json()
    try:
        # Validation de la liste de données numériques passée sous la clé 'data'
        values = validate_data(data)
        
        # Contrainte algorithmique : le test de Shapiro-Wilk devient instable ou non adapté au-delà de 5000 valeurs
        if len(values) > 5000:
            return jsonify({'erreur': 'Shapiro-Wilk limité à 5000 valeurs'}), 400
            
        # Calcul de la statistique W du test et de sa p-value
        stat, p_value = stats.shapiro(values)
        
        # Interprétation : si p_value > 0.05, on ne peut pas rejeter l'hypothèse nulle (donc la distribution suit une loi normale)
        result = {
            'statistique': round(float(stat), 6),                         # Statistique de test W proche de 1 si la distribution est normale
            'p_value': round(float(p_value), 6),                          # Seuil de décision statistique
            'est_normale': bool(p_value > 0.05),                          # Booléen exploitable par d'autres microservices en programmation
            'interpretation': "Distribution normale (p > 0.05)" if p_value > 0.05 else "Distribution non normale (p <= 0.05)"
        }
        
        return jsonify({'operation': 'test_normalite_shapiro_wilk', 'resultat': result})
        
    except (ValueError, TypeError) as e:
        # Capture d'exception robuste pour renvoyer un statut 400 propre en cas de mauvaise structure JSON
        return jsonify({'erreur': str(e)}), 400

# Point d'entrée de l'application Python
if __name__ == '__main__':
    # Lancement du serveur Web local Flask
    # port=5002 : évite les conflits avec le service 1 ou d'autres services réseau
    # debug=True : recharge automatiquement le code à chaque modification dans VS Code
    app.run(debug=True, port=5002)