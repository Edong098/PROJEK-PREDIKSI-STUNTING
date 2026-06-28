import streamlit as st
import pandas as pd
import importlib
import utils.visualization
importlib.reload(utils.visualization)
from utils.metrics import get_all_models_summary, get_model_evaluation, get_feature_importances, get_classes
from utils.visualization import plot_confusion_matrix, plot_feature_importance

def main():
    st.markdown('<h1 class="gradient-text" style="font-size: 2.8rem; margin-bottom: 0px;">MODEL EVALUATION</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-top: 5px; color: #FFFFFF; font-weight: 500;">Metrik Performa Baseline Model, Hyperparameter Tuning & Ensemble</h3>', unsafe_allow_html=True)
    st.write("---")

    # Muat ringkasan semua model yang sudah dilatih
    try:
        summary_df = get_all_models_summary()
        feature_imp = get_feature_importances()
        classes = get_classes()
    except Exception as e:
        st.error(f"Gagal memuat metrik model: {e}")
        return

    # Tampilkan kartu model terbaik
    best_model_name = summary_df.iloc[0]['Model']
    best_model_f1 = summary_df.iloc[0]['F1-Score (Macro)']
    
    st.markdown(
        f'<div class="glass-card" style="border-left: 6px solid #8E44AD; background-color: rgba(142, 68, 173, 0.08);">'
        f'<h4 style="color: #A55DD4; margin: 0 0 5px 0;">Model Terbaik Terpilih: {best_model_name}</h4>'
        f'<p style="color: #FFFFFF; margin: 0; line-height: 1.5; font-size: 0.9rem;">'
        f'Model ini dipilih secara otomatis karena memiliki nilai <strong>F1-Score (Macro) tertinggi ({best_model_f1:.4f})</strong> '
        f'di antara seluruh eksperimen. Pemilihan berbasis F1-Macro memastikan bahwa akurasi model tidak timpang sebelah (bias) '
        f'dan terbukti sangat sensitif dalam mendeteksi kelas-kelas penting berisiko tinggi (Stunted & Severely Stunted).'
        f'</p>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Tab untuk menampilkan rincian evaluasi
    tab_summary, tab_details = st.tabs(["📋 Tabel Perbandingan Performa", "🔬 Detail Metrik per Model"])

    with tab_summary:
        st.markdown("### 1. Tabel Perbandingan Metrik Evaluasi")
        st.write("Skor di bawah ini dikalkulasi dengan menguji performa prediksi model terlatih menggunakan data uji terpisah (test set).")
        
        # Tambahkan gaya highlight pada dataframe
        styled_df = summary_df.style.format({
            'Accuracy': '{:.4f}',
            'Precision': '{:.4f}',
            'Recall': '{:.4f}',
            'F1-Score (Macro)': '{:.4f}'
        })
        
        st.dataframe(styled_df, use_container_width=True)
        
        st.markdown(
            '<div class="glass-card" style="margin-top: 10px; border-top: 3px solid #2ECC71;">'
            '<h5>Analisis Hasil Perbandingan Model:</h5>'
            '<p style="font-size: 0.85rem; color: #FFFFFF; line-height: 1.6; margin: 0;">'
            '• <strong>Baseline vs Tuned:</strong> Penerapan pencarian parameter terbaik melalui <strong>GridSearchCV</strong> meningkatkan performa '
            'klasifikasi secara signifikan bagi semua model baseline.<br>'
            '• <strong>Ensemble Methods:</strong> Algoritma gabungan seperti <strong>Voting Classifier</strong> (menggabungkan prediksi probabilitas '
            'dari Logistic Regression, Decision Tree, dan Random Forest secara soft-voting) berhasil menyaring batas keputusan '
            'dan menghasilkan akurasi serta F1-Macro tertinggi.<br>'
            '• <strong>Evaluasi Metrik:</strong> Tingginya skor akurasi (mendekati 99%) disebabkan oleh relasi fisik yang sangat eksplisit '
            'antara variabel tinggi badan, usia, dan jenis kelamin terhadap standar gizi WHO yang tercatat di dataset.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

        # Bagian Feature Importance
        if feature_imp:
            st.markdown("---")
            st.markdown("### 2. Feature Importance (Pengaruh Variabel)")
            st.write("Tingkat kepentingan relatif dari variabel input dalam proses klasifikasi model Random Forest:")
            
            col_f1, col_f2 = st.columns([2, 1])
            with col_f1:
                fig_imp = plot_feature_importance(feature_imp)
                st.plotly_chart(fig_imp, use_container_width=True)
            with col_f2:
                st.markdown(
                    '<div class="glass-card" style="margin-top: 10px; height: 90%;">'
                    '<h5>Feature Importance:</h5>'
                    '<p style="font-size: 0.85rem; color: #FFFFFF; line-height: 1.5; margin: 0;">'
                    '1. <strong>Tinggi Badan (cm):</strong> Memiliki nilai kepentingan tertinggi (mendominasi). Hal ini dikarenakan stunting '
                    'secara klinis diukur berdasarkan deviasi tinggi badan anak terhadap standar tinggi umur seusianya.<br>'
                    '2. <strong>Umur (bulan):</strong> Berada di posisi kedua, karena tinggi badan balita harus dievaluasi secara dinamis '
                    'relatif terhadap pertambahan usianya.<br>'
                    '3. <strong>Jenis Kelamin:</strong> Berada di posisi terendah. Ini menunjukkan bahwa perbedaan anatomis laki-laki dan '
                    'perempuan memiliki pengaruh minor dalam pengelompokan pola stunting secara umum.'
                    '</p>'
                    '</div>',
                    unsafe_allow_html=True
                )

    with tab_details:
        st.markdown("### 3. Detail Metrik dan Visualisasi Matriks Kebingungan (Confusion Matrix)")
        
        model_names = summary_df['Model'].tolist()
        selected_model = st.selectbox(
            "Pilih Model untuk Menampilkan Detail Evaluasi:",
            model_names
        )
        
        eval_data = get_model_evaluation(selected_model)
        
        if eval_data:
            # Baris metrik utama
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("Accuracy", f"{eval_data['accuracy']:.4%}")
            with col_m2:
                st.metric("Precision (Macro)", f"{eval_data['precision']:.4%}")
            with col_m3:
                st.metric("Recall (Macro)", f"{eval_data['recall']:.4%}")
            with col_m4:
                st.metric("F1-Score (Macro)", f"{eval_data['f1_macro']:.4%}")
                
            st.markdown("---")
            
            col_r1, col_r2 = st.columns([1, 1])
            
            with col_r1:
                st.markdown("#### Classification Report Detail")
                report_dict = eval_data['classification_report']
                main_classes = {k: v for k, v in report_dict.items() if k not in ['accuracy', 'macro avg', 'weighted avg']}
                report_df = pd.DataFrame(main_classes).transpose()
                
                report_df['precision'] = report_df['precision'].map(lambda x: f"{x:.4f}")
                report_df['recall'] = report_df['recall'].map(lambda x: f"{x:.4f}")
                report_df['f1-score'] = report_df['f1-score'].map(lambda x: f"{x:.4f}")
                report_df['support'] = report_df['support'].map(lambda x: f"{int(x):,}")
                
                st.table(report_df)
                
                st.markdown(
                    '<div class="glass-card" style="margin-top: 10px;">'
                    '<h5>Classification Report:</h5>'
                    '<p style="font-size: 0.85rem; color: #FFFFFF; line-height: 1.5; margin: 0;">'
                    '• <strong>Precision:</strong> Mengukur persentase prediksi kelas tertentu yang benar. Contoh: Nilai precision tinggi pada kelas *stunted* berarti ketika model memprediksi anak stunted, probabilitas kebenaran klaim tersebut sangat tinggi.<br>'
                    '• <strong>Recall:</strong> Mengukur kemampuan model mendeteksi seluruh anggota aktual suatu kelas. Nilai recall tinggi pada kelas *severely stunted* sangat penting untuk menghindari kesalahan melewatkan anak yang sakit (false negative).<br>'
                    '• <strong>Support:</strong> Jumlah sampel asli kelas tersebut di data uji.'
                    '</p>'
                    '</div>',
                    unsafe_allow_html=True
                )
                
            with col_r2:
                # Tampilkan Confusion Matrix sebagai grafik
                fig_cm = plot_confusion_matrix(eval_data['confusion_matrix'], classes, title=f"Confusion Matrix: {selected_model}")
                st.plotly_chart(fig_cm, use_container_width=True)
                
                st.markdown(
                    '<div class="glass-card" style="margin-top: 10px;">'
                    '<h5>Confusion Matrix:</h5>'
                    '<p style="font-size: 0.85rem; color: #FFFFFF; line-height: 1.5; margin: 0;">'
                    '• <strong>Sumbu Vertikal (Aktual) vs Sumbu Horizontal (Prediksi)</strong>.<br>'
                    '• <strong>Diagonal Utama (Kiri-Atas ke Kanan-Bawah):</strong> Menunjukkan jumlah data yang berhasil diprediksi secara benar oleh model.<br>'
                    '• <strong>Elemen di luar Diagonal:</strong> Menunjukkan kesalahan prediksi (misklasifikasi). Sebagai contoh, jika terdapat nilai di kolom *stunted* baris *normal*, berarti model salah memprediksi balita normal sebagai stunted (false positive).'
                    '</p>'
                    '</div>',
                    unsafe_allow_html=True
                )
                
if __name__ == '__main__':
    main()
