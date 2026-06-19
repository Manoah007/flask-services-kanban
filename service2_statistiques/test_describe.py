import requests  # Importation de la bibliothèque cliente HTTP pour envoyer des requêtes à notre API

# Définition de l'URL absolue pointant vers la Route 1 de notre serveur local
url = "http://localhost:5002/stats/describe"

# Déclaration d'un jeu de données de test (Dictionnaire simulant le format JSON)
payload = {"data": [12.5, 15.3, 8.7, 21.0, 13.2, 9.8, 17.6, 11.4]}

# Envoi effectif de la requête POST avec l'argument 'json' qui s'occupe de sérialiser automatiquement notre dictionnaire
response = requests.post(url, json=payload)

# Affichage des métadonnées et du contenu de la réponse reçue dans le terminal VS Code
print("Status Code:", response.status_code)  # Doit afficher 200 si la validation et les calculs statistiques ont fonctionné
print("Réponse:", response.json())          # Affiche l'objet d'analyse statistique complet généré par l'API