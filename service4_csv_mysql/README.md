# Documentation Technique 
>  Microservice d'Importation de Données CSV (Service 4)

Ce composant est une API REST développée avec le framework **Flask**. Son rôle principal est de recevoir des fichiers CSV, d'appliquer des filtres de nettoyage et de validation rigoureux sur les données, puis de les stocker dans une base de données relationnelle **MySQL** (hébergée en local via XAMPP ou à distance via Alwaysdata).

---

## I - Architecture Générale et Configuration

###  Dépendances requises
Le service s'appuie sur les bibliothèques Python suivantes :

* `Flask` : Gestion du routage HTTP, interception des fichiers et génération des réponses JSON.  

* `pandas` : Analyse, structure sous forme de DataFrame, nettoyage et filtrage des données du fichier CSV.

* `mysql-connector-python` : Pilote natif de connexion et d'exécution des requêtes vers le serveur MySQL.

* `python-dotenv` : Chargement sécurisé des variables d'environnement à partir d'un fichier masqué.


### Variables d'environnement (`.env`)
L'application s'adapte à son infrastructure (développement local ou déploiement distant) sans aucune modification du code grâce aux variables suivantes :

* `DB_HOST` : Adresse du serveur de base de données (ex: `127.0.0.1` pour XAMPP ou `mysql-xxx.alwaysdata.net`).   

* `DB_USER` : Nom de l'utilisateur de la base de données (ex: `root`).  

* `DB_PASSWORD` : Mot de passe associé (laisser vide sous XAMPP par défaut).   

* `DB_NAME` : Nom de la base de données ciblée (ex: `r2.10_bd_tp2`).

### Constantes de Validation du Code

* `TAILLE_MAX_OCTETS` : Limite stricte fixée à **5 Mo** (`5 * 1024 * 1024` octets) pour éviter la saturation de la mémoire vive du serveur lors de la lecture des fichiers volumineux.  

* `COLONNES_REQUISES` : Le fichier CSV doit impérativement contenir au moins les colonnes `nom_serie` et `valeur`.

* `COLONNES_VALIDES` : Seules les données appartenant à `nom_serie`, `valeur`, `categorie` et `date_mesure` sont conservées. Toute autre colonne superflue est automatiquement ignorée lors du nettoyage.



## II - Spécifications des Endpoints de l'API

### 1 - Importation et traitement du CSV
Permet d'envoyer un fichier CSV à analyser, à nettoyer, puis à insérer dans la table SQL `donnees`.

* **URL :** `/upload/csv`  

* **Méthode :** `POST`

* **Type de contenu attendu (Payload) :** `multipart/form-data`

* **Structure :** Une clé nommée `"file"` contenant le fichier `.csv`.

#### Algorithme de traitement de la requête :
1. **Contrôle de structure :** Vérification de la présence de la clé `"file"`, d'un nom de fichier non vide et de l'extension globale `.csv`.  

2. **Contrôle de taille :** Lecture des octets pour s'assurer que le poids du fichier ne dépasse pas la constante des 5 Mo.

3. **Contrôle du schéma :** Lecture par *Pandas* via un flux de mémoire (`io.BytesIO`) et validation de la présence simultanée des colonnes `nom_serie` et `valeur`.

4. **Nettoyage et filtrage :** * Suppression des colonnes non autorisées (sécurité contre les injections de colonnes).

   * Conversion forcée de la colonne `valeur` en type numérique (`pd.to_numeric`).  

   * Suppression automatique des lignes dont la valeur est manquante, corrompue ou textuelle (les lignes *NaN* sont éliminées et comptabilisées dans `lignes_invalides_ignorees`).

5. **Persistance SQL :** Ouverture d’un curseur MySQL, itération sécurisée sur le DataFrame nettoyé et exécution séquentielle de la requête préparée `INSERT INTO` avant validation finale (`conn.commit()`).

#### Réponses HTTP types :

* **Succès (201 Created) :**
  ```json
    {
        "statut": "success",
        "lignes_inserees": 22,
        "lignes_invalides_ignorees": 0,
        "message": "22 ligne(s) chargée(s) dans la table donnees"
    }
  ```

* **Erreur Client (400 Bad Request) - Exemple (Extension invalide)**
  ```json
    {
        "erreur": "Seuls les fichiers .csv sont acceptés"
    }
    ```

* **Erreur Client (413 Payload Too Large)**
  ```json
    {
    "erreur": "Fichier trop volumineux (max 5 Mo)"
    }
  ```

* **Erreur Serveur (500 Internal Server Error) - Problème de connexion SQL**
  ```json
    {
    "erreur": "Erreur base de données",
    "detail": "1049 (42000): Unknown database 'r2.10_bd_tp2'"
    }
  ```

### 2 - Consultation des Séries Enregistrées
Permet d'obtenir une vue d'ensemble et des indicateurs sur les données présentes en base, agrégées par série.

* URL : ```/upload/series```  

* Méthode : ```GET```

#### Fonctionnement
Le service établit une connexion à la base de données et exécute une requête de regroupement SQL (```GROUP BY nom_serie```). Elle calcule dynamiquement le volume de points injectés (```COUNT(*)```) ainsi que les bornes temporelles (première date ```MIN()``` et dernière date ```MAX()```) de chaque série disponible, triées par ordre alphabétique.

#### Réponse HTTP type
* **Succès (200 OK)**
  ```json
    {
    "series": [
        {
        "serie": "temperature_exterieure",
        "n_points": 140,
        "debut": "2026-06-01",
        "fin": "2026-06-15"
        }
    ],
    "total": 1
    }
  ```

## III - Schéma de la Table SQL Cible

Pour que le service fonctionne de manière nominale, la table SQL suivante doit impérativement exister au sein de la base de données MySQL configurée (locale ou distante)

```SQL
    CREATE TABLE donnees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nom_serie VARCHAR(255) NOT NULL,
        valeur FLOAT NOT NULL,
        categorie VARCHAR(255) NULL,
        date_mesure VARCHAR(255) NULL
    );
```

## IV - Guide de Recette (Tests via commandes Curl)
### Démarrage du service
Après avoir activé l'environnement virtuel (venv) et correctement configuré et sauvegardé le fichier .env, lancez le script d'écoute

```PowerShell
    python app.py
```

> Le serveur s'exécute en mode debug sur le port 5004.


### Test 1 : Envoyer un fichier CSV (Terminal de test)

```PowerShell
    curl.exe -X POST http://localhost:5004/upload/csv -F "file=@data/donnees_exemple.csv"
```

### Test 2 : Consulter les séries stockées

```PowerShell
    curl.exe http://localhost:5004/upload/series*
```