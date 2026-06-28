import pandas as pd
import numpy as np

def clean_string(df):
    """
    Membersihkan kolom kategori string dengan mengubah ke huruf kecil (lowercase)
    dan menghapus spasi di awal/akhir nilai.
    """
    df_clean = df.copy()
    if 'Jenis Kelamin' in df_clean.columns:
        df_clean['Jenis Kelamin'] = df_clean['Jenis Kelamin'].astype(str).str.strip().str.lower()
    if 'Status Gizi' in df_clean.columns:
        df_clean['Status Gizi'] = df_clean['Status Gizi'].astype(str).str.strip().str.lower()
    return df_clean

def fill_missing(df, numeric_medians=None, categorical_modes=None):
    """
    Mengimputasi nilai yang hilang (missing values).
    Fitur numerik diisi dengan nilai median.
    Fitur kategorikal diisi dengan nilai modus (mode).
    """
    df_clean = df.copy()
    numeric_cols = df_clean.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = df_clean.select_dtypes(include=['object']).columns
    
    if numeric_medians is None:
        numeric_medians = {col: df_clean[col].median() for col in numeric_cols if not df_clean[col].isnull().all()}
    if categorical_modes is None:
        categorical_modes = {}
        for col in categorical_cols:
            mode_val = df_clean[col].mode()
            categorical_modes[col] = mode_val[0] if not mode_val.empty else "unknown"

    for col in numeric_cols:
        if col in numeric_medians:
            df_clean[col] = df_clean[col].fillna(numeric_medians[col])
            
    for col in categorical_cols:
        if col in categorical_modes:
            df_clean[col] = df_clean[col].fillna(categorical_modes[col])
            
    return df_clean, numeric_medians, categorical_modes

def remove_duplicate(df):
    """
    Menghapus baris duplikat dari dataset.
    """
    return df.drop_duplicates().reset_index(drop=True)

def remove_outlier_iqr(df):
    """
    Mengidentifikasi dan menghapus outlier (pencilan) menggunakan metode IQR
    untuk kolom Umur dan Tinggi Badan.
    """
    df_clean = df.copy()
    outlier_mask = pd.Series(False, index=df_clean.index)
    bounds = {}
    
    for col in ['Umur (bulan)', 'Tinggi Badan (cm)']:
        if col in df_clean.columns:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            bounds[col] = (lower_bound, upper_bound)
            col_outlier = ~df_clean[col].between(lower_bound, upper_bound)
            outlier_mask = outlier_mask | col_outlier
            
    df_clean = df_clean[~outlier_mask].reset_index(drop=True)
    return df_clean, bounds

def preprocess(df):
    """
    Menerapkan pipeline pembersihan dan preprocessing lengkap ke seluruh dataset.
    """
    # 1. Bersihkan nilai string
    df_clean = clean_string(df)
    # 2. Isi nilai yang hilang
    df_clean, _, _ = fill_missing(df_clean)
    # 3. Hapus data duplikat
    df_clean = remove_duplicate(df_clean)
    # 4. Filter data berdasarkan rentang nilai yang valid
    from preprocessing.validation import filter_valid_range
    df_clean = filter_valid_range(df_clean)
    # 5. Hapus outlier (pencilan)
    df_clean, _ = remove_outlier_iqr(df_clean)
    return df_clean

def prepare_prediction_input(umur, gender, tinggi, scaler, le_gender, feature_columns):
    """
    Melakukan encoding dan scaling pada fitur input pengguna untuk keperluan prediksi model.
    """
    gender_clean = str(gender).strip().lower()
    
    # Label encode kolom jenis kelamin
    gender_encoded = le_gender.transform([gender_clean])[0]
    
    # Buat dataframe input dari nilai yang dimasukkan
    input_data = pd.DataFrame([{
        'Umur (bulan)': float(umur),
        'Jenis Kelamin': int(gender_encoded),
        'Tinggi Badan (cm)': float(tinggi)
    }])
    
    # Urutkan kolom agar sesuai urutan yang diharapkan oleh scaler/model
    input_data = input_data[feature_columns]
    
    # Lakukan scaling pada input
    input_scaled = scaler.transform(input_data)
    
    # Kembalikan sebagai DataFrame untuk mempertahankan nama fitur dan menghindari peringatan scikit-learn
    return pd.DataFrame(input_scaled, columns=feature_columns)
