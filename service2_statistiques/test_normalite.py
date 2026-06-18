import requests

url = "http://localhost:5002/stats/test_normalite"
# Une série de données pour tester la distribution
payload = {
    "data": [10, 12, 15, 14, 13, 11, 12, 14, 15, 13]
}

response = requests.post(url, json=payload)
print("Status Code:", response.status_code)
print("Réponse:", response.json())