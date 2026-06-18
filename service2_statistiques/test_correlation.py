import requests

url = "http://localhost:5002/stats/correlation"
# Exemple de deux séries de données de même taille pour le test
payload = {
    "x": [10, 12, 15, 18, 20],
    "y": [22, 25, 30, 33, 40]
}

response = requests.post(url, json=payload)
print("Status Code:", response.status_code)
print("Réponse:", response.json())