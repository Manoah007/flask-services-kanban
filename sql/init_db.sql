-- 1. On supprime l'ancienne base de données erronée si elle existe
DROP DATABASE IF EXISTS flask_stats;

-- 2. On recrée la base de données proprement
CREATE DATABASE flask_stats
 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 3. On se positionne sur la nouvelle base
USE flask_stats;

-- 4. On crée la table avec la colonne 'categorie' (et pas 'type_mesure')
CREATE TABLE donnees ( 
    id INT AUTO_INCREMENT PRIMARY KEY, 
    nom_serie VARCHAR(100) NOT NULL, 
    valeur DECIMAL(12,4) NOT NULL, 
    categorie VARCHAR(50) DEFAULT NULL, 
    date_mesure DATE DEFAULT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

-- 5. On insère TOUTES les données de test initiales (Série A ET Série B)
INSERT INTO donnees (nom_serie, valeur, categorie, date_mesure) VALUES
('serie_A', 12.50, 'temp', '2024-01-15'),
('serie_A', 15.30, 'temp', '2024-01-16'),
('serie_A', 8.70, 'temp', '2024-01-17'),
('serie_A', 21.00, 'temp', '2024-01-18'),
('serie_A', 13.20, 'temp', '2024-01-19'),
('serie_B', 45.10, 'pression', '2024-01-15'),
('serie_B', 52.80, 'pression', '2024-01-16'),
('serie_B', 48.60, 'pression', '2024-01-17'),
('serie_B', 55.20, 'pression', '2024-01-18');