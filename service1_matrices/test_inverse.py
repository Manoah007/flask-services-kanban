import urllib.request  # Importe le module qui permet d’envoyer des requêtes HTTP en Python
import json  # Importe le module qui permet de manipuler des données JSON

url = "http://localhost:5001/matrices/inverse"  # Définit l’adresse de la route Flask à tester

data = {  # Crée les données qui seront envoyées à l’API
    "A": [[1, 2], [3, 4]]  # Définit la matrice A dont on veut calculer l’inverse
}  # Fin du dictionnaire contenant la matrice

req = urllib.request.Request(  # Crée une requête HTTP vers l’API
    url,  # Indique l’URL de la route à appeler
    data=json.dumps(data).encode("utf-8"),  # Transforme les données Python en JSON puis les encode en UTF-8
    headers={"Content-Type": "application/json"},  # Précise que les données envoyées sont au format JSON
    method="POST"  # Indique que la requête utilise la méthode POST
)  # Fin de la création de la requête

with urllib.request.urlopen(req) as response:  # Envoie la requête à l’API et récupère la réponse
    result = json.loads(response.read().decode("utf-8"))  # Lit la réponse, la décode, puis la transforme en dictionnaire Python
    print(result)  # Affiche le résultat renvoyé par l’API