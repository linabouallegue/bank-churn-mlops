# Bank Churn Prediction - Streamlit App

Application Streamlit pour tester et démontrer l'API de prédiction de churn bancaire.

## 🚀 Démarrage rapide

### 1. Installation des dépendances
```bash
pip install -r requirements_streamlit.txt
```

### 2. Lancement de l'application
```bash
streamlit run streamlit_app.py
```

L'application sera accessible sur : http://localhost:8501

## 📋 Prérequis

- **API FastAPI** doit être démarrée sur `http://localhost:8000`
- **Python 3.8+**
- **Streamlit** installé

## 🎯 Fonctionnalités

### 🔮 Prédiction Individuelle
- Interface intuitive pour saisir les caractéristiques d'un client
- Prédiction en temps réel avec probabilité de churn
- Niveau de risque (Low/Medium/High)
- Visualisation claire des résultats

### 📊 Prédictions par Lot
- Analyse de plusieurs clients simultanément
- Chargement d'exemples de données
- Résultats présentés sous forme de tableau

### 📈 Statistiques API
- Métriques de performance de l'API
- Nombre de prédictions effectuées
- Temps de fonctionnement
- État du modèle

## 🏗️ Architecture

```
┌─────────────────┐    HTTP     ┌─────────────────┐
│   Streamlit     │ ──────────► │    FastAPI      │
│   Frontend      │             │     API         │
└─────────────────┘             └─────────────────┘
                                   │
                                   ▼
                            ┌─────────────────┐
                            │  ML Model      │
                            │ (Random Forest)│
                            └─────────────────┘
```

## 🎨 Interface Utilisateur

- **Design moderne** avec sidebar navigation
- **Responsive** pour différentes tailles d'écran
- **Feedback visuel** avec couleurs et icônes
- **Validation en temps réel** des données saisies

## 🔧 Variables du Client

L'application permet de saisir toutes les variables nécessaires :

- **Score de crédit** (300-850)
- **Âge** (18-100 ans)
- **Ancienneté** (0-10 ans)
- **Solde bancaire** (€)
- **Nombre de produits** (1-4)
- **Carte de crédit** (Oui/Non)
- **Membre actif** (Oui/Non)
- **Salaire estimé** (€)
- **Pays** (France/Espagne/Allemagne)
- **Genre** (Homme/Femme)

## 📊 Résultats

Pour chaque prédiction, l'application affiche :
- **Probabilité de churn** (en pourcentage)
- **Prédiction binaire** (Départ/Rester)
- **Niveau de risque** (Low/Medium/High avec couleurs)

## 🐳 Utilisation avec Docker

Si vous utilisez Docker pour l'API :

```bash
# Terminal 1 : API
docker run -d -p 8000:8000 bank-churn-mlops:v6

# Terminal 2 : Streamlit
pip install -r requirements_streamlit.txt
streamlit run streamlit_app.py
```

## 📈 Monitoring

L'onglet "Statistiques API" permet de suivre :
- Nombre total de prédictions
- Prédictions par lot
- Uptime de l'API
- État du modèle chargé

## 🎯 Cas d'usage

Cette application est idéale pour :
- **Tests fonctionnels** de l'API
- **Démonstrations** aux stakeholders
- **Validation** des prédictions du modèle
- **Interface utilisateur** pour les analystes métier

---

*Développé pour le projet MLOps Bank Churn Prediction*