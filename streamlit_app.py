#!/usr/bin/env python3
"""
Streamlit App for Bank Churn Prediction
Interface utilisateur pour tester l'API de prédiction de churn bancaire
"""

import streamlit as st
import requests
import json
import pandas as pd
import time
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Bank Churn Predictor",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration API
API_BASE_URL = "https://bank-churn-mlops-ftx6sqc5dveyrzponyudod.streamlit.app/"

# Fonctions utilitaires
def call_api(endpoint, data=None):
    """Appel à l'API avec gestion d'erreur"""
    try:
        if data:
            response = requests.post(f"{API_BASE_URL}{endpoint}", json=data, timeout=10)
        else:
            response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion: {str(e)}")
        return None

def get_customer_features():
    """Interface pour saisir les caractéristiques du client"""
    st.header("📊 Caractéristiques du Client")

    col1, col2, col3 = st.columns(3)

    with col1:
        credit_score = st.slider("Score de crédit", 300, 850, 650, help="Score de crédit du client (300-850)")
        age = st.slider("Âge", 18, 100, 35, help="Âge du client en années")
        tenure = st.slider("Ancienneté", 0, 10, 5, help="Nombre d'années de relation bancaire")

    with col2:
        balance = st.number_input("Solde (€)", 0.0, 1000000.0, 50000.0, step=1000.0, help="Solde du compte bancaire")
        num_of_products = st.slider("Nombre de produits", 1, 4, 1, help="Nombre de produits bancaires utilisés")
        has_cr_card = st.selectbox("Carte de crédit", ["Oui", "Non"], help="Le client possède-t-il une carte de crédit?")
        has_cr_card = 1 if has_cr_card == "Oui" else 0

    with col3:
        is_active_member = st.selectbox("Membre actif", ["Oui", "Non"], help="Le client est-il un membre actif?")
        is_active_member = 1 if is_active_member == "Oui" else 0
        estimated_salary = st.number_input("Salaire estimé (€)", 0.0, 200000.0, 50000.0, step=1000.0, help="Salaire annuel estimé")

    # Variables catégorielles
    st.subheader("📍 Informations géographiques")
    col4, col5 = st.columns(2)

    with col4:
        geography = st.selectbox("Pays", ["France", "Spain", "Germany"], help="Pays de résidence")

    with col5:
        gender = st.selectbox("Genre", ["Female", "Male"], help="Genre du client")

    # Conversion des variables catégorielles
    geography_france = 1 if geography == "France" else 0
    geography_spain = 1 if geography == "Spain" else 0
    geography_germany = 1 if geography == "Germany" else 0
    gender_male = 1 if gender == "Male" else 0

    return {
        "CreditScore": credit_score,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": num_of_products,
        "HasCrCard": has_cr_card,
        "IsActiveMember": is_active_member,
        "EstimatedSalary": estimated_salary,
        "Geography_Germany": geography_germany,
        "Geography_Spain": geography_spain
    }

def display_prediction_result(result):
    """Affichage du résultat de prédiction"""
    if not result:
        return

    st.header("🎯 Résultat de la Prédiction")

    col1, col2, col3 = st.columns(3)

    with col1:
        churn_prob = result.get('churn_probability', 0)
        st.metric("Probabilité de départ", f"{churn_prob:.1%}")

    with col2:
        prediction = result.get('prediction', 0)
        if prediction == 1:
            st.error("🔴 Prédiction: DÉPART")
        else:
            st.success("🟢 Prédiction: RESTE")

    with col3:
        risk_level = result.get('risk_level', 'Unknown')
        if risk_level == 'High':
            st.error(f"⚠️ Risque: {risk_level}")
        elif risk_level == 'Medium':
            st.warning(f"⚠️ Risque: {risk_level}")
        else:
            st.success(f"✅ Risque: {risk_level}")

def display_api_stats():
    """Affichage des statistiques de l'API"""
    st.header("📈 Statistiques de l'API")

    stats = call_api("/stats")
    if stats:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Prédictions totales", stats.get('total_predictions', 0))

        with col2:
            st.metric("Prédictions batch", stats.get('total_batch_predictions', 0))

        with col3:
            uptime = stats.get('uptime_seconds', 0)
            hours = int(uptime // 3600)
            minutes = int((uptime % 3600) // 60)
            st.metric("Temps de fonctionnement", f"{hours}h {minutes}m")

        with col4:
            model_loaded = "✅ Chargé" if stats.get('model_loaded', False) else "❌ Non chargé"
            st.metric("Modèle", model_loaded)

        if stats.get('last_prediction'):
            st.info(f"📅 Dernière prédiction: {stats['last_prediction']}")

def batch_prediction_interface():
    """Interface pour les prédictions par lot"""
    st.header("📊 Prédictions par Lot")

    # Exemple de données
    sample_data = [
        {
            "CreditScore": 650, "Age": 35, "Tenure": 5, "Balance": 50000,
            "NumOfProducts": 1, "HasCrCard": 1, "IsActiveMember": 1,
            "EstimatedSalary": 50000, "Geography_Germany": 0, "Geography_Spain": 0
        },
        {
            "CreditScore": 700, "Age": 45, "Tenure": 8, "Balance": 75000,
            "NumOfProducts": 2, "HasCrCard": 1, "IsActiveMember": 0,
            "EstimatedSalary": 80000, "Geography_Germany": 0, "Geography_Spain": 1
        }
    ]

    if st.button("🔄 Charger des exemples"):
        st.session_state.batch_data = sample_data
        st.success("Exemples chargés !")

    # Affichage des données
    if 'batch_data' in st.session_state and st.session_state.batch_data:
        st.subheader("Données à analyser")
        df = pd.DataFrame(st.session_state.batch_data)
        st.dataframe(df)

        if st.button("🚀 Lancer l'analyse par lot"):
            with st.spinner("Analyse en cours..."):
                result = call_api("/predict/batch", st.session_state.batch_data)

            if result:
                st.success(f"✅ Analyse terminée pour {result.get('count', 0)} clients")

                # Affichage des résultats
                predictions_df = pd.DataFrame(result.get('predictions', []))
                if not predictions_df.empty:
                    st.subheader("Résultats")
                    st.dataframe(predictions_df)

def main():
    """Fonction principale"""
    st.title("🏦 Bank Churn Prediction")
    st.markdown("---")

    # Sidebar
    st.sidebar.title("🔧 Configuration")
    st.sidebar.markdown("---")

    # Test de connexion API
    api_status = call_api("/")
    if api_status:
        st.sidebar.success("✅ API connectée")
        st.sidebar.json(api_status)
    else:
        st.sidebar.error("❌ API non accessible")
        st.sidebar.info("Vérifiez que l'API est démarrée sur http://localhost:8000")
        return

    # Navigation
    page = st.sidebar.radio("Navigation", ["Prédiction Individuelle", "Prédictions par Lot", "Statistiques API"])

    if page == "Prédiction Individuelle":
        # Formulaire de saisie
        customer_data = get_customer_features()

        # Bouton de prédiction
        if st.button("🔮 Faire la prédiction", type="primary", use_container_width=True):
            with st.spinner("Analyse en cours..."):
                result = call_api("/predict", customer_data)

            if result:
                display_prediction_result(result)

                # Affichage des données envoyées
                with st.expander("📋 Données analysées"):
                    st.json(customer_data)

    elif page == "Prédictions par Lot":
        batch_prediction_interface()

    elif page == "Statistiques API":
        display_api_stats()

        # Bouton refresh
        if st.button("🔄 Actualiser"):
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("*Application développée pour le projet MLOps Bank Churn Prediction*")
    st.markdown("*API FastAPI + Modèle Random Forest + Docker*")

if __name__ == "__main__":
    main()