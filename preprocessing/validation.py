import pandas as pd

def validate_input(umur, gender, tinggi):
    """
    Validates user input values for stunting prediction.
    """
    errors = []
    
    # Validate Age
    if not (0 <= umur <= 60):
        errors.append("Umur harus berada di antara 0 dan 60 bulan.")
        
    # Validate Gender
    if gender.lower() not in ['laki-laki', 'perempuan']:
        errors.append("Jenis kelamin harus 'Laki-laki' atau 'Perempuan'.")
        
    # Validate Height
    if not (40.0 <= tinggi <= 130.0):
        errors.append("Tinggi badan harus berada di antara 40 dan 130 cm.")
        
    return len(errors) == 0, errors

def filter_valid_range(df):
    """
    Filters the dataset to only include rows with logically valid values as in the notebook.
    """
    valid_gender = ['laki-laki', 'perempuan']
    valid_status = ['normal', 'stunted', 'severely stunted', 'tinggi']
    
    mask = pd.Series(True, index=df.index)
    
    if 'Umur (bulan)' in df.columns:
        mask = mask & df['Umur (bulan)'].between(0, 60)
    if 'Tinggi Badan (cm)' in df.columns:
        mask = mask & df['Tinggi Badan (cm)'].between(40, 130)
    if 'Jenis Kelamin' in df.columns:
        mask = mask & df['Jenis Kelamin'].isin(valid_gender)
    if 'Status Gizi' in df.columns:
        mask = mask & df['Status Gizi'].isin(valid_status)
        
    return df[mask].reset_index(drop=True)
