import requests

url = "http://localhost:5002/stats/describe"
payload = {"data": [12.5, 15.3, 8.7, 21.0, 13.2, 9.8, 17.6, 11.4]}

response = requests.post(url, json=payload)
print("Status Code:", response.status_code)
print("Réponse:", response.json())