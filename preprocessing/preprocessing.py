import pandas as pd
import numpy as np

def clean_string(df):
    """
    Cleans string categories by converting to lowercase and stripping whitespaces.
    """
    df_clean = df.copy()
    if 'Jenis Kelamin' in df_clean.columns:
        df_clean['Jenis Kelamin'] = df_clean['Jenis Kelamin'].astype(str).str.strip().str.lower()
    if 'Status Gizi' in df_clean.columns:
        df_clean['Status Gizi'] = df_clean['Status Gizi'].astype(str).str.strip().str.lower()
    return df_clean

def fill_missing(df, numeric_medians=None, categorical_modes=None):
    """
    Imputes missing values.
    Numeric features are filled with medians.
    Categorical features are filled with mode.
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
    Removes duplicate rows from the dataset.
    """
    return df.drop_duplicates().reset_index(drop=True)

def remove_outlier_iqr(df):
    """
    Identifies and removes outliers based on the IQR method for Age and Height.
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
    Applies the full cleaning and preprocessing pipeline to the dataset.
    """
    # 1. Clean string values
    df_clean = clean_string(df)
    # 2. Fill missing values
    df_clean, _, _ = fill_missing(df_clean)
    # 3. Remove duplicates
    df_clean = remove_duplicate(df_clean)
    # 4. Filter by valid range
    from preprocessing.validation import filter_valid_range
    df_clean = filter_valid_range(df_clean)
    # 5. Remove outliers
    df_clean, _ = remove_outlier_iqr(df_clean)
    return df_clean

def prepare_prediction_input(umur, gender, tinggi, scaler, le_gender, feature_columns):
    """
    Encodes and scales user input features for model prediction.
    """
    gender_clean = str(gender).strip().lower()
    
    # Label encode gender
    gender_encoded = le_gender.transform([gender_clean])[0]
    
    # Construct input dataframe
    input_data = pd.DataFrame([{
        'Umur (bulan)': float(umur),
        'Jenis Kelamin': int(gender_encoded),
        'Tinggi Badan (cm)': float(tinggi)
    }])
    
    # Reorder columns to match features expected by scaler/model
    input_data = input_data[feature_columns]
    
    # Scale input
    input_scaled = scaler.transform(input_data)
    
    # Return as DataFrame to preserve feature names and suppress scikit-learn warnings
    return pd.DataFrame(input_scaled, columns=feature_columns)
