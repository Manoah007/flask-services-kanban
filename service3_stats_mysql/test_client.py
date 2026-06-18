import requests

BASE_URL = "http://localhost:5003/db/stats"

print("========================================")
print("🧪 TEST ROUTE 1 : DESCRIBE (serie_A)")
print("========================================")
reponse_describe = requests.get(f"{BASE_URL}/describe?serie=serie_A")
print(f"Code HTTP : {reponse_describe.status_code}")
print(reponse_describe.json())

print("\n========================================")
print("🧪 TEST ROUTE 2 : CORRELATION (serie_A & serie_B)")
print("========================================")
reponse_correlation = requests.get(f"{BASE_URL}/correlation?serie_x=serie_A&serie_y=serie_B")
print(f"Code HTTP : {reponse_correlation.status_code}")
print(reponse_correlation.json())