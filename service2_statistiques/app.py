from flask import Flask, request, jsonify
import numpy as np
from scipy import stats

app = Flask(__name__)

# Fonction utilitaire pour valider les données reçues
def validate_data(data, key='data'):
    """Valide et retourne une liste de nombres."""
    if key not in data:
        raise ValueError(f"Clé '{key}' manquante dans la requête")
    values = data[key]
    if not isinstance(values, list) or len(values) < 2:
        raise ValueError("'data' doit être une liste d'au moins 2 valeurs")
    return np.array(values, dtype=float)

# Route 1 — Description statistique
@app.route('/stats/describe', methods=['POST'])
def describe():
    data = request.get_json()
    try:
        values = validate_data(data)
        result = {
            'n': int(len(values)),
            'moyenne': round(float(np.mean(values)), 4),
            'mediane': round(float(np.median(values)), 4),
            'ecart_type': round(float(np.std(values, ddof=1)), 4),
            'variance': round(float(np.var(values, ddof=1)), 4),
            'minimum': round(float(np.min(values)), 4),
            'maximum': round(float(np.max(values)), 4),
            'q1': round(float(np.percentile(values, 25)), 4),
            'q3': round(float(np.percentile(values, 75)), 4),
            'etendue': round(float(np.ptp(values)), 4),
        }
        return jsonify({'operation': 'description', 'resultat': result})
    
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


# Route 2 — Corrélation de Pearson
@app.route('/stats/correlation', methods=['POST'])
def correlation():
    data = request.get_json()
    try:
        # On valide la présence et le format des deux séries de données 'x' et 'y'
        x_values = validate_data(data, key='x')
        y_values = validate_data(data, key='y')
        
        if len(x_values) != len(y_values):
            return jsonify({'erreur': 'Les listes x et y doivent avoir la même taille'}), 400
            
        # Calcul du coefficient de Pearson et de la p-value avec scipy
        corr_coeff, p_value = stats.pearsonr(x_values, y_values)
        
        result = {
            'coefficient': round(float(corr_coeff), 4),
            'p_value': round(float(p_value), 4),
            'interpretation': "Corrélation américaine significative" if p_value < 0.05 else "Corrélation non significative"
        }
        
        return jsonify({'operation': 'correlation', 'resultat': result})
        
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400
    
    # Route 3 — Test de normalité (Shapiro-Wilk)
@app.route('/stats/test_normalite', methods=['POST'])
def test_normalite():
    data = request.get_json()
    try:
        values = validate_data(data)
        
        # Limite théorique du test de Shapiro-Wilk
        if len(values) > 5000:
            return jsonify({'erreur': 'Shapiro-Wilk limité à 5000 valeurs'}), 400
            
        # Calcul de la statistique et de la p-value
        stat, p_value = stats.shapiro(values)
        
        result = {
            'statistique': round(float(stat), 6),
            'p_value': round(float(p_value), 6),
            'est_normale': bool(p_value > 0.05),
            'interpretation': "Distribution normale (p > 0.05)" if p_value > 0.05 else "Distribution non normale (p <= 0.05)"
        }
        
        return jsonify({'operation': 'test_normalite_shapiro_wilk', 'resultat': result})
        
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400

if __name__ == '__main__':
    # On utilise le port 5002 attribué au Service 2 
    app.run(debug=True, port=5002)
