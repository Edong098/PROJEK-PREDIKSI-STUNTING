import streamlit as st
import pandas as pd
from utils.loader import load_dataset
from preprocessing.preprocessing import clean_string, fill_missing, remove_duplicate, remove_outlier_iqr
from preprocessing.validation import filter_valid_range

def main():
    st.markdown('<h1 class="gradient-text" style="font-size: 2.8rem; margin-bottom: 0px;">DATASET OVERVIEW</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-top: 5px; color: #FFFFFF; font-weight: 500;">Audit Data dan Preprocessing Eksploratif</h3>', unsafe_allow_html=True)
    st.write("---")

    # Load dataset
    try:
        df_raw = load_dataset()
    except Exception as e:
        st.error(f"Gagal memuat dataset: {e}")
        return

    # Process Cleaned Data Dynamically to compute metrics
    df_step1 = clean_string(df_raw)
    df_step2, _, _ = fill_missing(df_step1)
    
    # Calculate stats
    raw_shape = df_raw.shape
    raw_duplicates = df_raw.duplicated().sum()
    raw_nulls = df_raw.isnull().sum().sum()
    
    # Cleaning pipeline steps
    df_step3 = remove_duplicate(df_step2)
    df_step4 = filter_valid_range(df_step3)
    df_clean, bounds = remove_outlier_iqr(df_step4)
    
    clean_shape = df_clean.shape
    clean_duplicates = df_clean.duplicated().sum()
    clean_nulls = df_clean.isnull().sum().sum()
    
    # Tabs for view
    view_tab, audit_tab = st.tabs(["👁️ Preview Dataset", "🔍 Audit & Preprocessing Stats"])
    
    with view_tab:
        st.markdown("#### Preview Data Bersih (Cleaned & Filtered)")
        st.dataframe(df_clean.head(100), use_container_width=True)
        st.caption(f"Menampilkan 100 baris pertama dari total {clean_shape[0]:,} baris data hasil pembersihan.")

    with audit_tab:
        st.markdown("### Perbandingan Sebelum & Sesudah Preprocessing")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🟥 Sebelum (Data Mentah)")
            st.markdown(
                f'<div class="glass-card" style="border-left: 5px solid #E74C3C;">'
                f'<p><strong>Dimensi:</strong> {raw_shape[0]:,} baris × {raw_shape[1]} kolom</p>'
                f'<p><strong>Jumlah Duplikat:</strong> {raw_duplicates:,} baris</p>'
                f'<p><strong>Missing Values:</strong> {raw_nulls} data</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        with col2:
            st.markdown("#### 🟩 Sesudah (Data Bersih)")
            st.markdown(
                f'<div class="glass-card" style="border-left: 5px solid #2ECC71;">'
                f'<p><strong>Dimensi:</strong> {clean_shape[0]:,} baris × {clean_shape[1]} kolom</p>'
                f'<p><strong>Jumlah Duplikat:</strong> {clean_duplicates} baris (Dihapus)</p>'
                f'<p><strong>Missing Values:</strong> {clean_nulls} data (Dihilangkan)</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown("### Detail Langkah Preprocessing")
        st.markdown(f"""
        1. **Pembersihan String**: Casing kolom *Jenis Kelamin* dan *Status Gizi* diubah menjadi lowercase dan spasi ujung dihilangkan.
        2. **Imputasi Data Hilang (Missing Value)**:
           - Fitur numerik diimputasi menggunakan nilai **Median**.
           - Fitur kategorikal diimputasi menggunakan nilai **Mode (Modus)**.
        3. **Penghapusan Duplikat**: Menghapus **{raw_duplicates:,}** baris data duplikat agar model tidak mengalami overfitting pada data yang redundan.
        4. **Validasi Rentang (Range Validation)**:
           - Umur dibatasi di rentang: **0 - 60 bulan**.
           - Tinggi Badan dibatasi di rentang: **40 - 130 cm**.
           - Kategori Status Gizi harus berupa: *normal, stunted, severely stunted, tinggi*.
        5. **Penghapusan Outlier (Pencilan)**: Menggunakan metode *Interquartile Range (IQR)* dengan faktor 1.5.
           - Batas Umur: **{bounds.get('Umur (bulan)', (0,0))[0]:.2f}** hingga **{bounds.get('Umur (bulan)', (0,0))[1]:.2f}** bulan.
           - Batas Tinggi Badan: **{bounds.get('Tinggi Badan (cm)', (0,0))[0]:.2f}** hingga **{bounds.get('Tinggi Badan (cm)', (0,0))[1]:.2f}** cm.
        """)

        # Distribution comparison
        st.markdown("### Ringkasan Informasi Kolom")
        info_df = pd.DataFrame({
            "Kolom": df_raw.columns,
            "Tipe Data": [str(t) for t in df_raw.dtypes],
            "Non-Null Count": df_raw.notnull().sum().values,
            "Nilai Unik (Raw)": [df_raw[col].nunique() for col in df_raw.columns],
            "Nilai Unik (Clean)": [df_clean[col].nunique() if col in df_clean.columns else "N/A" for col in df_raw.columns]
        })
        st.table(info_df)

if __name__ == '__main__':
    main()
