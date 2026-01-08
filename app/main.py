from datetime import datetime
import time
import logging
import os
import hashlib
import json
from functools import lru_cache
import joblib
import numpy as np
from typing import List
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.models import CustomerFeatures, PredictionResponse

# Statistiques de monitoring
prediction_stats = {
    "total_predictions": 0,
    "total_batch_predictions": 0,
    "start_time": datetime.now(),
    "last_prediction": None
}

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Charge le modele au demarrage de l'API et nettoie a la fermeture"""
    global model
    try:
        model = joblib.load(MODEL_PATH)
        logger.info(f"Modele charge avec succes depuis {MODEL_PATH}")
    except Exception as e:
        logger.error(f"Erreur lors du chargement du modele : {e}")
        model = None
    yield
    # Nettoyage si necessaire
    logger.info("Arret de l'API")

app = FastAPI(
    title="Bank Churn Prediction API",
    description="API de prediction de defaillance client",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS pour permettre les requetes depuis un navigateur
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modele au demarrage
MODEL_PATH = os.getenv("MODEL_PATH", "model/churn_model.pkl")
model = None


@app.get("/", tags=["General"])
def root():
    """Endpoint racine"""
    return {
        "message": "Bank Churn Prediction API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health", tags=["General"])
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/stats", tags=["Monitoring"])
def get_stats():
    """Statistiques d'utilisation de l'API"""
    uptime = datetime.now() - prediction_stats["start_time"]
    
    return {
        "uptime_seconds": uptime.total_seconds(),
        "total_predictions": prediction_stats["total_predictions"],
        "total_batch_predictions": prediction_stats["total_batch_predictions"],
        "last_prediction": prediction_stats["last_prediction"],
        "model_loaded": model is not None
    }

def hash_features(features_dict: dict) -> str:
    """Cree un hash unique pour les features"""
    return hashlib.md5(
        json.dumps(features_dict, sort_keys=True).encode()
    ).hexdigest()

# Cache pour les predictions (1000 dernieres)
@lru_cache(maxsize=1000)
def predict_cached(features_hash: str, features_json: str):
    features_dict = json.loads(features_json)
    input_data = np.array([[
        features_dict["CreditScore"],
        features_dict["Age"],
        features_dict["Tenure"],
        features_dict["Balance"],
        features_dict["NumOfProducts"],
        features_dict["HasCrCard"],
        features_dict["IsActiveMember"],
        features_dict["EstimatedSalary"],
        features_dict["Geography_Germany"],
        features_dict["Geography_Spain"]
    ]])
    
    proba = model.predict_proba(input_data)[0, 1]
    prediction = int(proba > 0.5)
    
    if proba < 0.3:
        risk = "Low"
    elif proba < 0.7:
        risk = "Medium"
    else:
        risk = "High"
    
    return {
        "churn_probability": round(float(proba), 4),
        "prediction": prediction,
        "risk_level": risk
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(features: CustomerFeatures):
    features_dict = features.dict()
    features_hash = hash_features(features_dict)
    features_json = json.dumps(features_dict)
    
    # Utilise le cache si disponible
    result = predict_cached(features_hash, features_json)
    
    logger.info(f"Prediction - Hash: {features_hash[:8]}")
    return result

@app.post("/predict/batch", tags=["Prediction"])
def predict_batch(features_list: List[CustomerFeatures]):
    """
    Predictions en batch pour plusieurs clients
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Modele non disponible")
    
    try:
        predictions = []
        
        for features in features_list:
            input_data = np.array([[
                features.CreditScore, features.Age, features.Tenure,
                features.Balance, features.NumOfProducts, features.HasCrCard,
                features.IsActiveMember, features.EstimatedSalary,
                features.Geography_Germany, features.Geography_Spain
            ]])
            
            proba = model.predict_proba(input_data)[0, 1]
            prediction = int(proba > 0.5)
            
            predictions.append({
                "churn_probability": round(float(proba), 4),
                "prediction": prediction
            })
        
        logger.info(f"Batch prediction : {len(predictions)} clients traites")
        
        # Mise a jour des stats
        prediction_stats["total_batch_predictions"] += len(predictions)
        prediction_stats["last_prediction"] = datetime.now().isoformat()
        
        return {"predictions": predictions, "count": len(predictions)}
    
    except Exception as e:
        logger.error(f"Erreur batch prediction : {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)