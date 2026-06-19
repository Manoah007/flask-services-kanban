# Microservice Statistiques (Service 2)

Ce microservice fait partie d'une architecture orientée services développée dans le cadre du TP de Gestion de projet (R2.10). Il est entièrement dédié aux calculs statistiques et aux analyses de données, exposé via une API REST propulsée par **Flask**, **NumPy** et **SciPy**.

Le service s'exécute de manière autonome sur le port **5002**.

---

## 🚀 Fonctionnalités

Le microservice fournit trois routes principales accessibles en méthode `POST`. Toutes les données transitent au format JSON.

### 1. Description Statistique (`/stats/describe`)
Calcule les indicateurs statistiques descriptifs fondamentaux d'une série de données numériques unique.
* **Indicateurs calculés :** Nombre d'éléments ($n$), moyenne arithmétique, médiane, écart-type corrigé ($ddof=1$), variance corrigée ($ddof=1$), minimum, maximum, premier quartile ($Q1$), troisième quartile ($Q3$) et étendue.
* **Sécurité :** Validation de la présence de la clé, du type de données (liste) et d'un nombre minimal de 2 valeurs.

### 2. Corrélation de Pearson (`/stats/correlation`)
Évalue la force et le sens de la relation linéaire entre deux variables continues $x$ et $y$.
* **Vérification :** Contrôle de l'égalité de taille entre la série $x$ et la série $y$.
* **Interprétation :** Fournit le coefficient de corrélation de Pearson ($r$) et sa $p\text{-value}$. Une interprétation automatique est ajoutée si le résultat est significatif ($p < 0.05$).

### 3. Test de Normalité de Shapiro-Wilk (`/stats/test_normalite`)
Vérifie si un échantillon de données suit une distribution gaussienne (loi normale).
* **Contrainte :** Limité à un échantillon maximal de 5 000 valeurs conformément aux limites théoriques et de stabilité de l'algorithme de Shapiro-Wilk.
* **Interprétation :** Si la $p\text{-value} > 0.05$, la distribution est considérée comme normale (on ne rejette pas l'hypothèse nulle $H_0$).

---

## 🛠️ Prérequis et Installation

### Dépendances requises
Assurez-vous d'avoir Python 3.x installé, ainsi que les bibliothèques suivantes :
```bash
pip install flask numpy scipy requests


service2_statistiques/
├── app.py                  # Code principal de l'API Flask
├── test_describe.py        # Script de test unitaire pour la description
├── test_correlation.py     # Script de test unitaire pour la corrélation
└── test_normalite.py       # Script de test unitaire pour la normalité