import os
import pickle
import json
import pandas as pd
import streamlit as st

@st.cache_resource
def load_model():
    """
    Loads and caches the model package pickle file.
    The package contains:
      - 'model': The best estimator model.
      - 'scaler': Fitted StandardScaler.
      - 'le_gender': LabelEncoder for gender.
      - 'le_status': LabelEncoder for status gizi.
      - 'feature_columns': List of expected feature columns.
      - 'model_name': Best model name (string).
    """
    possible_paths = [
        os.path.join("model", "model_stunting.pkl"),
        "model_stunting.pkl",
        os.path.join("..", "model", "model_stunting.pkl")
    ]
    
    model_path = None
    for path in possible_paths:
        if os.path.exists(path):
            model_path = path
            break
            
    if model_path is None:
        raise FileNotFoundError("File model_stunting.pkl tidak ditemukan di direktori mana pun.")
        
    with open(model_path, "rb") as file:
        model_package = pickle.load(file)
    return model_package

@st.cache_data
def load_dataset():
    """
    Loads and caches the raw dataset.
    """
    possible_paths = [
        os.path.join("data", "data_balita.csv"),
        "data_balita.csv",
        os.path.join("..", "data", "data_balita.csv")
    ]
    
    data_path = None
    for path in possible_paths:
        if os.path.exists(path):
            data_path = path
            break
            
    if data_path is None:
        raise FileNotFoundError("File data_balita.csv tidak ditemukan di direktori mana pun.")
        
    df = pd.read_csv(data_path)
    return df

@st.cache_data
def load_metrics_data():
    """
    Loads and caches the offline model evaluation metrics from metrics_data.json.
    """
    possible_paths = [
        os.path.join("utils", "metrics_data.json"),
        "metrics_data.json",
        os.path.join("..", "utils", "metrics_data.json")
    ]
    
    json_path = None
    for path in possible_paths:
        if os.path.exists(path):
            json_path = path
            break
            
    if json_path is None:
        raise FileNotFoundError("File metrics_data.json tidak ditemukan di direktori mana pun.")
        
    with open(json_path, "r") as file:
        data = json.load(file)
    return data
