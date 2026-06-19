import requests  # Utilisation de la librairie d'émulation de client HTTP

# URL de destination ciblant notre Route 3 (Algorithme statistique de Shapiro-Wilk)
url = "http://localhost:5002/stats/test_normalite"

# Échantillon de test configuré sous forme de dictionnaire JSON pour analyser sa distribution
payload = {
    "data": [10, 12, 15, 14, 13, 11, 12, 14, 15, 13]
}

# Envoi de l'échantillon par méthode POST au serveur local Flask
response = requests.post(url, json=payload)

# Impression du diagnostic réseau et logique renvoyé par l'API
print("Status Code:", response.status_code)  # Attendu : 200 OK
print("Réponse:", response.json())          # Affiche les valeurs statistiques calculées ainsi que le booléen 'est_normale'