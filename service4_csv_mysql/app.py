import io
import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, jsonify, request

# Chargement de l'environnement et initialisation
load_dotenv()
app = Flask(__name__)

# Constantes de configuration
COLONNES_REQUISES = {"nom_serie", "valeur"}
COLONNES_VALIDES = {"nom_serie", "valeur", "categorie", "date_mesure"}
TAILLE_MAX_OCTETS = 5 * 1024 * 1024  # 5 Mo


def get_connection():
    """Crée et retourne une connexion à la base de données MySQL."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


@app.route("/upload/csv", methods=["POST"])
def upload_csv():
    """ 
    Cette fonction permet de recevoir un fichier CSV, de le faire passer
    par plusieurs critères de validations, puis de l'insérer dans la base de données MySQL.
    """

    #Vérifier la présence du fichier dans la requête
    if "file" not in request.files:
        return (
            jsonify({"erreur": 'Aucun fichier envoyé (clé "file" manquante)'}),
            400,
        )

    file = request.files["file"]

    # Vérifier le nom de fichier et l'extension
    if file.filename == "":
        return jsonify({"erreur": "Nom de fichier vide"}), 400

    # Vérifier l'extension du fichier
    if not file.filename.endswith(".csv"):
        return jsonify({"erreur": "Seuls les fichiers .csv sont acceptés"}), 400

    # Lire et valider le contenu CSV
    try:
        content = file.read()
        if len(content) > TAILLE_MAX_OCTETS:
            return jsonify({"erreur": "Fichier trop volumineux (max 5 Mo)"}), 413

        df = pd.read_csv(io.BytesIO(content)) #Création d'un DataFrame à partir du contenu CSV

    except Exception as e:
        return jsonify({"erreur": f"Lecture CSV impossible : {e}"}), 400

    # Vérifier les colonnes obligatoires
    colonnes_manquantes = COLONNES_REQUISES - set(df.columns)
    if colonnes_manquantes:
        return (
            jsonify(
                {
                    "erreur": "Colonnes obligatoires manquantes",
                    "manquantes": list(colonnes_manquantes),
                }
            ),
            400,
        )

    # Nettoyer et filtrer les données
    df = df[[c for c in df.columns if c in COLONNES_VALIDES]].copy()

    # Conversion de la colonne 'valeur' en numérique et gestion des erreurs
    df["valeur"] = pd.to_numeric(df["valeur"], errors="coerce")
    lignes_invalides = df["valeur"].isna().sum()
    df.dropna(subset=["valeur"], inplace=True)

    if df.empty:
        return jsonify({"erreur": "Aucune ligne valide dans le CSV"}), 400

    # Insérer les données nettoyées dans MySQL
    try:
        conn = get_connection()
        cursor = conn.cursor()
        insertions = 0

        query = (
            "INSERT INTO donnees (nom_serie, valeur, categorie, date_mesure) "
            "VALUES (%s, %s, %s, %s)"
        )

        for _, row in df.iterrows():
            params = (
                str(row["nom_serie"]),
                float(row["valeur"]),
                (
                    str(row["categorie"])
                    if "categorie" in df.columns and pd.notna(row["categorie"])
                    else None
                ),
                (
                    str(row["date_mesure"])
                    if "date_mesure" in df.columns
                    and pd.notna(row["date_mesure"])
                    else None
                ),
            )
            cursor.execute(query, params)
            insertions += 1

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        return (
            jsonify({"erreur": "Erreur base de données", "detail": str(e)}),
            500,
        )

    # Réponse en cas de succès
    return (
        jsonify(
            {
                "statut": "success",
                "lignes_inserees": insertions,
                "lignes_invalides_ignorees": int(lignes_invalides),
                "message": f"{insertions} ligne(s) chargée(s) dans la table donnees",
            }
        ),
        201,
    )


if __name__ == "__main__":
    # Changement de port pour correspondre à votre configuration (5004)
    app.run(debug=True, port=5004)

# Charger le fichier CSV de démonstration curl -X POST http://localhost:5004/upload/csv \ -F 'file=@data/donnees_exemple.csv'
# Réponse attendue :
# {
#   "statut": "success",
#   "lignes_inserees": 22,
#   "lignes_invalides_ignorees": 0,
#   "message": "22 ligne(s) chargée(s) dans la table donnees"
# }
# Lister les séries disponibles curl http://localhost:5004/upload/series

