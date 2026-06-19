from flask import Flask, request, jsonify  # Importe Flask pour créer l'API, request pour récupérer les données envoyées, et jsonify pour renvoyer du JSON
import numpy as np  # Importe NumPy pour faire les calculs sur les matrices

app = Flask(__name__)  # Crée l'application Flask principale

def parse_matrix(data, key):  # Définit une fonction qui récupère une matrice dans les données JSON
    """Convertit une liste de listes en tableau NumPy."""  # Explique le rôle de la fonction
    try:  # Essaie de convertir la matrice
        return np.array(data[key], dtype=float)  # Récupère la matrice avec sa clé et la transforme en tableau NumPy de nombres flottants
    except (KeyError, ValueError) as e:  # Si la clé n'existe pas ou si la conversion échoue
        raise ValueError(f"Matrice '{key}' invalide : {e}")  # Renvoie une erreur claire indiquant que la matrice est invalide

@app.route('/matrices/add', methods=['POST'])  # Crée la route POST pour additionner deux matrices
def add_matrices():  # Définit la fonction appelée quand on utilise la route /matrices/add
    data = request.get_json()  # Récupère les données JSON envoyées dans la requête

    try:  # Essaie d'exécuter le calcul
        A = parse_matrix(data, 'A')  # Récupère et convertit la matrice A
        B = parse_matrix(data, 'B')  # Récupère et convertit la matrice B

        if A.shape != B.shape:  # Vérifie si les deux matrices ont les mêmes dimensions
            return jsonify({'erreur': 'Dimensions incompatibles'}), 400  # Renvoie une erreur si les dimensions sont différentes

        result = (A + B).tolist()  # Additionne les deux matrices puis transforme le résultat en liste Python

        return jsonify({  # Renvoie la réponse au format JSON
            'operation': 'addition',  # Indique l'opération effectuée
            'resultat': result  # Renvoie le résultat de l'addition
        })

    except (ValueError, TypeError) as e:  # Si une erreur arrive pendant le traitement
        return jsonify({'erreur': str(e)}), 400  # Renvoie le message d'erreur au format JSON
    
@app.route('/matrices/multiply', methods=['POST'])  # Crée la route POST pour multiplier deux matrices
def multiply_matrices():  # Définit la fonction appelée pour la multiplication
    data = request.get_json()  # Récupère les données JSON envoyées par le client

    try:  # Essaie d'exécuter le calcul
        A = parse_matrix(data, 'A')  # Récupère et convertit la matrice A
        B = parse_matrix(data, 'B')  # Récupère et convertit la matrice B

        if A.shape[1] != B.shape[0]:  # Vérifie si le nombre de colonnes de A correspond au nombre de lignes de B
            return jsonify({'erreur': 'Colonnes(A) doit egaler Lignes(B)'}), 400  # Renvoie une erreur si la multiplication est impossible

        result = np.dot(A, B).tolist()  # Multiplie les deux matrices avec NumPy puis convertit le résultat en liste

        return jsonify({  # Renvoie la réponse au format JSON
            'operation': 'multiplication',  # Indique que l'opération est une multiplication
            'resultat': result  # Renvoie le résultat de la multiplication
        })

    except (ValueError, TypeError) as e:  # Si une erreur arrive pendant la multiplication
        return jsonify({'erreur': str(e)}), 400  # Renvoie l'erreur au format JSON
    
@app.route('/matrices/transpose', methods=['POST'])  # Crée la route POST pour transposer une matrice
def transpose_matrix():  # Définit la fonction appelée pour la transposition
    data = request.get_json()  # Récupère les données JSON envoyées dans la requête

    try:  # Essaie d'exécuter la transposition
        A = parse_matrix(data, 'A')  # Récupère et convertit la matrice A

        result = A.T.tolist()  # Transpose la matrice avec .T puis convertit le résultat en liste

        return jsonify({  # Renvoie la réponse en JSON
            'operation': 'transposee',  # Indique que l'opération est une transposition
            'resultat': result  # Renvoie la matrice transposée
        })

    except (ValueError, TypeError) as e:  # Si une erreur arrive pendant le traitement
        return jsonify({'erreur': str(e)}), 400  # Renvoie l'erreur au format JSON
    
@app.route('/matrices/determinant', methods=['POST'])  # Crée la route POST pour calculer le déterminant
def determinant_matrix():  # Définit la fonction appelée pour le déterminant
    data = request.get_json()  # Récupère les données JSON envoyées par le client

    try:  # Essaie d'exécuter le calcul
        A = parse_matrix(data, 'A')  # Récupère et convertit la matrice A

        if A.shape[0] != A.shape[1]:  # Vérifie si la matrice est carrée
            return jsonify({'erreur': 'La matrice doit etre carree'}), 400  # Renvoie une erreur si la matrice n'est pas carrée

        det = np.linalg.det(A)  # Calcule le déterminant de la matrice avec NumPy

        return jsonify({  # Renvoie la réponse au format JSON
            'operation': 'determinant',  # Indique que l'opération est un déterminant
            'resultat': round(det, 6)  # Renvoie le déterminant arrondi à 6 chiffres après la virgule
        })

    except (ValueError, TypeError) as e:  # Si une erreur arrive pendant le calcul
        return jsonify({'erreur': str(e)}), 400  # Renvoie l'erreur au format JSON

@app.route('/matrices/inverse', methods=['POST'])  # Crée la route POST pour calculer l'inverse d'une matrice
def inverse_matrix():  # Définit la fonction appelée pour l'inverse
    data = request.get_json()  # Récupère les données JSON envoyées dans la requête

    try:  # Essaie d'exécuter le calcul
        A = parse_matrix(data, 'A')  # Récupère et convertit la matrice A

        if A.shape[0] != A.shape[1]:  # Vérifie si la matrice est carrée
            return jsonify({'erreur': 'La matrice doit etre carree'}), 400  # Renvoie une erreur si la matrice n'est pas carrée

        det = np.linalg.det(A)  # Calcule le déterminant pour savoir si la matrice est inversible

        if abs(det) < 1e-10:  # Vérifie si le déterminant est proche de 0
            return jsonify({'erreur': 'Matrice singuliere, non inversible'}), 400  # Renvoie une erreur si la matrice n'est pas inversible

        result = np.linalg.inv(A).tolist()  # Calcule l'inverse de la matrice puis convertit le résultat en liste

        return jsonify({  # Renvoie la réponse au format JSON
            'operation': 'inverse',  # Indique que l'opération est une inversion
            'resultat': result  # Renvoie la matrice inverse
        })

    except (ValueError, TypeError) as e:  # Si une erreur arrive pendant le traitement
        return jsonify({'erreur': str(e)}), 400  # Renvoie l'erreur au format JSON

if __name__ == '__main__':  # Vérifie que le fichier est lancé directement
    app.run(debug=True, port=5001)  # Lance le serveur Flask en mode debug sur le port 5001