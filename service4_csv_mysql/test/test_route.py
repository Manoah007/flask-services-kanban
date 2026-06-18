import io
import pytest
from app import app  # On importe l'application Flask

@pytest.fixture
def client():
    """Cette fixture configure le client de test Flask.
    Elle s'exécutera automatiquement avant chaque fonction de test."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Test unitaire route - upload/csv #

def test_upload_csv_missing_file_key(client):
    """Vérifie le comportement si la clé 'file' est manquante dans la requête."""
    # On envoie une requête POST vide (sans dictionnaire de fichiers)
    response = client.post("/upload/csv", data={})
    
    assert response.status_code == 400
    assert "Aucun fichier envoyé" in response.json["erreur"]


def test_upload_csv_invalid_extension(client):
    """Vérifie qu'un fichier qui n'est pas un .csv est bien rejeté."""
    data = {
        "file": (io.BytesIO(b"contenu factice"), "photo.png")
    }
    response = client.post("/upload/csv", data=data, content_type="multipart/form-data")
    
    assert response.status_code == 400
    assert "Seuls les fichiers .csv sont acceptés" in response.json["erreur"]


def test_upload_csv_corrupted_or_empty_values(client):
    """Vérifie le cas où le CSV ne contient aucune ligne valide (valeurs textuelles)."""
    
    csv_invalide = "nom_serie,valeur,categorie,date_mesure\nserie_A,pas_un_nombre,test,2026-06-18"
    
    data = {
        "file": (io.BytesIO(csv_invalide.encode("utf-8")), "test_corrompu.csv")
    }
    response = client.post("/upload/csv", data=data, content_type="multipart/form-data")
    
    assert response.status_code == 400
    assert "Aucune ligne valide dans le CSV" in response.json["erreur"]


# Test unitaire route - upload/series #

def test_list_series_structure(client):
    """Vérifie que la route GET retourne une structure JSON conforme (200 OK)."""
    response = client.get("/upload/series")
    
    assert response.status_code == 200
    assert "series" in response.json
    assert "total" in response.json
    assert isinstance(response.json["series"], list)