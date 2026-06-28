import streamlit as st
import pandas as pd
import numpy as np
import datetime
from utils.loader import load_model
from preprocessing.preprocessing import prepare_prediction_input
from preprocessing.validation import validate_input
from preprocessing.helper import get_stunting_interpretation
from utils.visualization import plot_confidence_gauge, plot_probability_distribution, plot_probability_pie, plot_feature_importance

def main():
    st.markdown('<h1 class="gradient-text" style="font-size: 2.8rem; margin-bottom: 0px;">PREDIKSI STATUS GIZI</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-top: 5px; color: #FFFFFF; font-weight: 500;">Sistem Deteksi Risiko Stunting Balita</h3>', unsafe_allow_html=True)
    st.write("---")

    # Muat Paket Model Machine Learning
    try:
        model_package = load_model()
        model = model_package["model"]
        scaler = model_package["scaler"]
        le_gender = model_package["le_gender"]
        le_status = model_package["le_status"]
        feature_columns = model_package["feature_columns"]
        model_name = model_package["model_name"]
    except Exception as e:
        st.error(f"Gagal memuat file model ML: {e}")
        return

    # Inisialisasi Session State untuk input formulir
    if "umur_input" not in st.session_state:
        st.session_state.umur_input = 24
    if "gender_input" not in st.session_state:
        st.session_state.gender_input = "Laki-laki"
    if "tinggi_input" not in st.session_state:
        st.session_state.tinggi_input = 82.0
    if "prediction_done" not in st.session_state:
        st.session_state.prediction_done = False

    st.markdown("### 1. Form Input Data Balita")
    
    # Wadah formulir input
    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            umur = st.number_input(
                "Umur Balita (bulan):",
                min_value=0,
                max_value=60,
                key="umur_input",
                step=1,
                help="Masukkan usia balita dalam rentang 0 hingga 60 bulan."
            )
            
        with col2:
            gender = st.selectbox(
                "Jenis Kelamin:",
                options=["Laki-laki", "Perempuan"],
                key="gender_input",
                help="Pilih jenis kelamin balita."
            )
            
        with col3:
            tinggi = st.number_input(
                "Tinggi Badan (cm):",
                min_value=40.0,
                max_value=130.0,
                key="tinggi_input",
                step=0.1,
                format="%.1f",
                help="Masukkan tinggi badan balita dalam rentang 40.0 hingga 130.0 cm."
            )
            
        submit_btn = st.form_submit_button("Prediksi Status Gizi")

    # Jika tombol prediksi ditekan
    if submit_btn:
        # 1. Validasi Input Pengguna
        is_valid, errors = validate_input(umur, gender, tinggi)
        
        if not is_valid:
            for err in errors:
                st.error(err)
        else:
            # 2. Tampilkan spinner loading
            with st.spinner("Menganalisis karakteristik tumbuh kembang balita..."):
                try:
                    # 3. Jalankan preprocessing dan encoding fitur
                    gender_model_input = "laki-laki" if gender == "Laki-laki" else "perempuan"
                    X_scaled = prepare_prediction_input(umur, gender_model_input, tinggi, scaler, le_gender, feature_columns)
                    
                    # 4. Jalankan prediksi model
                    pred_idx = model.predict(X_scaled)[0]
                    status_gizi = le_status.inverse_transform([pred_idx])[0]
                    
                    # 5. Ekstrak probabilitas jika model mendukungnya
                    probs_dict = {}
                    confidence_pct = 100.0
                    
                    if hasattr(model, "predict_proba"):
                        probs = model.predict_proba(X_scaled)[0]
                        max_idx = np.argmax(probs)
                        confidence_pct = probs[max_idx] * 100
                        
                        for idx, prob in enumerate(probs):
                            class_label = le_status.inverse_transform([idx])[0]
                            probs_dict[class_label] = prob * 100
                    else:
                        probs_dict = {status_gizi: 100.0}
                        
                    prediction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    advice_text = get_stunting_interpretation(status_gizi, confidence_pct, model_name)
                    
                    # 6. Simpan hasil prediksi ke session state
                    st.session_state.status_gizi = status_gizi
                    st.session_state.confidence_pct = confidence_pct
                    st.session_state.probs_dict = probs_dict
                    st.session_state.prediction_time = prediction_time
                    st.session_state.advice_text = advice_text
                    st.session_state.gender_model_input = gender_model_input
                    st.session_state.prediction_done = True
                    
                    st.toast("Prediksi berhasil dilakukan!", icon="✅")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses prediksi: {e}")

    # Jika hasil prediksi tersedia di Session State, tampilkan hasilnya
    if st.session_state.prediction_done:
        # Ambil variabel dari session state
        umur_val = st.session_state.umur_input
        gender_val = st.session_state.gender_input
        tinggi_val = st.session_state.tinggi_input
        status_gizi = st.session_state.status_gizi
        confidence_pct = st.session_state.confidence_pct
        probs_dict = st.session_state.probs_dict
        prediction_time = st.session_state.prediction_time
        advice_text = st.session_state.advice_text
        gender_model_input = st.session_state.gender_model_input
        
        st.write("---")
        st.markdown("### Hasil Analisis Gizi & Stunting")

        # 2. Kartu Ringkasan Prediksi
        # Tentukan warna status (warna cerah agar terbaca pada tema gelap)
        status_label = status_gizi.title()
        if "Normal" in status_label:
            bg_color = "rgba(46, 204, 113, 0.08)"
            border_color = "#2ECC71"
            text_color = "#2ECC71" # Hijau Neon
        elif "Severely Stunted" in status_label:
            bg_color = "rgba(231, 76, 60, 0.08)"
            border_color = "#E74C3C"
            text_color = "#FF7675" # Merah Koral Terang
        elif "Stunted" in status_label:
            bg_color = "rgba(243, 156, 18, 0.08)"
            border_color = "#F39C12"
            text_color = "#F39C12" # Oranye Terang
        else: # Tinggi
            bg_color = "rgba(52, 152, 219, 0.08)"
            border_color = "#3498DB"
            text_color = "#74B9FF" # Biru Terang

        st.markdown(
            f'<div class="glass-card" style="border: 2px solid {border_color}; background-color: {bg_color};">'
            f'<h4 style="color: #FFFFFF; margin: 0; font-size: 0.9rem; text-transform: uppercase;">Status Gizi Terprediksi</h4>'
            f'<h1 style="color: {text_color}; margin: 5px 0 10px 0; font-size: 3rem; font-weight: 800;">{status_label}</h1>'
            f'<div style="display: flex; gap: 40px; margin-top: 15px; flex-wrap: wrap;">'
            f'<div><span style="color: #FFFFFF; font-size: 0.85rem;">Confidence Score:</span><br><strong style="font-size: 1.1rem; color: #FFFFFF;">{confidence_pct:.2f}%</strong></div>'
            f'<div><span style="color: #FFFFFF; font-size: 0.85rem;">Algoritma Model:</span><br><strong style="font-size: 1.1rem; color: #FFFFFF;">{model_name}</strong></div>'
            f'<div><span style="color: #FFFFFF; font-size: 0.85rem;">Waktu Analisis:</span><br><strong style="font-size: 1.1rem; color: #FFFFFF;">{prediction_time}</strong></div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        
        # 3. Gauge Kepercayaan & 4. Distribusi Probabilitas (Kolom)
        col_g1, col_g2 = st.columns([1, 1])
        
        with col_g1:
            st.markdown("#### 3. Confidence Gauge")
            fig_gauge = plot_confidence_gauge(confidence_pct)
            st.plotly_chart(fig_gauge, use_container_width=True)
            
        with col_g2:
            st.markdown("#### 4. Distribusi Probabilitas Kelas")
            fig_dist = plot_probability_distribution(probs_dict)
            st.plotly_chart(fig_dist, use_container_width=True)
            
        # 5. Pie Chart & 6. Feature Importance (Kolom)
        col_p1, col_p2 = st.columns([1, 1])
        
        with col_p1:
            st.markdown("#### 5. Komposisi Probabilitas")
            fig_pie = plot_probability_pie(probs_dict)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_p2:
            st.markdown("#### 6. Feature Importance Model")
            if hasattr(model, "feature_importances_"):
                feat_importances = dict(zip(feature_columns, model.feature_importances_))
                fig_imp = plot_feature_importance(feat_importances)
                st.plotly_chart(fig_imp, use_container_width=True)
            else:
                from utils.metrics import get_feature_importances
                pre_computed_imp = get_feature_importances()
                if pre_computed_imp:
                    fig_imp = plot_feature_importance(pre_computed_imp)
                    st.plotly_chart(fig_imp, use_container_width=True)
                    st.caption("Menampilkan profil korelasi fitur global dari model Random Forest dasar sebagai referensi.")
                else:
                    st.info("Fitur Importance tidak tersedia untuk model ini.")
 
        # 7. Ringkasan Data Input
        st.markdown("#### 7. Ringkasan Data Input Pengguna")
        summary_input_df = pd.DataFrame({
            "Fitur Pengukuran": ["Umur Balita", "Jenis Kelamin", "Tinggi Badan"],
            "Nilai Input": [f"{umur_val} Bulan", gender_val, f"{tinggi_val:.1f} cm"]
        })
        st.table(summary_input_df)
 
        # 8. Hasil & Rekomendasi Medis
        st.markdown("#### 8. Hasil & Rekomendasi Medis")
        
        # Tampilkan komponen alert yang sesuai dengan status
        if "severely stunted" in status_gizi.lower():
            st.error(advice_text)
        elif "stunted" in status_gizi.lower():
            st.warning(advice_text)
        elif "normal" in status_gizi.lower():
            st.success(advice_text)
        else: # tinggi
            st.info(advice_text)
 
        # 9. Reset Input Data
        st.write("---")
        st.markdown("#### 9. Reset Data Input")
        reset_btn = st.button("Input Data Baru (Reset)", use_container_width=True, help="Hapus hasil analisis saat ini dan reset semua form input.")
        if reset_btn:
            # Hapus semua variabel session state yang relevan
            keys_to_reset = ["umur_input", "gender_input", "tinggi_input", "prediction_done",
                             "status_gizi", "confidence_pct", "probs_dict",
                             "prediction_time", "advice_text", "gender_model_input"]
            for k in keys_to_reset:
                if k in st.session_state:
                    del st.session_state[k]
            # Inisialisasi ulang nilai default
            st.session_state.umur_input = 24
            st.session_state.gender_input = "Laki-laki"
            st.session_state.tinggi_input = 82.0
            st.session_state.prediction_done = False
            st.rerun()


if __name__ == '__main__':
    main()
