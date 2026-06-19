import requests  # Importation du client HTTP requests

# Définition de l'URL ciblant la Route 2 dédiée à l'analyse de corrélation linéaire de Pearson
url = "http://localhost:5002/stats/correlation"

# Configuration du payload avec deux clés distinctes ('x' et 'y') contenant des listes de tailles identiques
payload = {
    "x": [10, 12, 15, 18, 20],
    "y": [22, 25, 30, 33, 40]
}

# Transmission des données à l'API via une requête HTTP de type POST
response = requests.post(url, json=payload)

# Sortie console pour valider les résultats de notre test
print("Status Code:", response.status_code)  # Attendu : 200 OK
print("Réponse:", response.json())          # Doit afficher le coefficient r de Pearson proche de 1 et une p-value significative