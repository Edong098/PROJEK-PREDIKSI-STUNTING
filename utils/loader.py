import os
import pickle
import json
import pandas as pd
import streamlit as st

@st.cache_resource
def load_model():
    """
    Memuat dan melakukan cache terhadap file pickle paket model.
    Paket ini berisi:
      - 'model': Model estimator terbaik yang telah dilatih.
      - 'scaler': Objek StandardScaler yang sudah di-fit.
      - 'le_gender': LabelEncoder untuk kolom jenis kelamin.
      - 'le_status': LabelEncoder untuk kolom status gizi.
      - 'feature_columns': Daftar nama kolom fitur yang diharapkan.
      - 'model_name': Nama model terbaik (string).
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
    Memuat dan melakukan cache terhadap dataset mentah.
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
    Memuat dan melakukan cache terhadap data metrik evaluasi model offline dari metrics_data.json.
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
