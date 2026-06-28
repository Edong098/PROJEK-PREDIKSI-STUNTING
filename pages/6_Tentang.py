import streamlit as st
import os

def main():
    st.markdown('<h1 class="gradient-text" style="font-size: 2.8rem; margin-bottom: 0px;">TENTANG TIM PENELITI</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-top: 5px; font-weight: 500;">Anggota Kelompok Tugas Akhir UAS Data Mining Lanjut</h3>', unsafe_allow_html=True)
    st.write("---")

    # Deskripsi dan logo aplikasi
    st.markdown("""
        <div style="padding-top: 10px;">
            <h3 style="margin: 0;">Sistem Prediksi Status Gizi Anak Balita</h3>
            <p style="line-height: 1.6; margin-top: 5px;">
                Aplikasi ini dikembangkan sebagai bentuk pemenuhan tugas Ujian Akhir Semester (UAS) pada mata kuliah 
                <strong>Data Mining Lanjut</strong>. Pendekatan machine learning yang diimplementasikan bertujuan untuk 
                menyelesaikan permasalahan sosial riil di Indonesia, yaitu stunting pada balita.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("### Kontribusi Anggota Kelompok")

    st.markdown("""
    <style>
        .profile-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
        }
        .profile-grid .glass-card {
            min-height: 260px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        @media (max-width: 768px) {
            .profile-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    <div class="profile-grid">
        <div class="glass-card" style="border-left: 5px solid #2ECC71;">
            <h4 style="margin: 0;">👤 Anggota 1 - Nizellya Salfani (2301010014)</h4>
            <p style="font-size: 0.85rem; font-weight: bold; text-transform: uppercase; margin: 3px 0;">Data Understanding & Data Audit</p>
            <p style="font-size: 0.9rem; line-height: 1.5;">Bertanggung jawab dalam memuat dataset awal, memeriksa struktur tabel, mengidentifikasi tipe data, mendeteksi jumlah missing values dan data duplikat mula-mula, serta menghitung rasio ketidakseimbangan kelas target.</p>
        </div>
        <div class="glass-card" style="border-left: 5px solid #E74C3C;">
            <h4 style="margin: 0;">👤 Anggota 2 - Anggi Rahmawati (2301010001)</h4>
            <p style="font-size: 0.85rem; font-weight: bold; text-transform: uppercase; margin: 3px 0;">Data Cleaning & Preprocessing</p>
            <p style="font-size: 0.9rem; line-height: 1.5;">Melakukan standarisasi penulisan string, imputasi data hilang (median & mode), penghapusan duplikat, validasi batas logis rentang nilai, deteksi dan eliminasi pencilan (outliers) berbasis IQR, standard scaling, serta penanganan ketidakseimbangan kelas menggunakan SMOTE.</p>
        </div>
        <div class="glass-card" style="border-left: 5px solid #3498DB;">
            <h4 style="margin: 0;">👤 Anggota 3 - Daffa Dhiya Ulhaq (2301010024)</h4>
            <p style="font-size: 0.85rem; font-weight: bold; text-transform: uppercase; margin: 3px 0;">Exploratory Data Analysis (EDA)</p>
            <p style="font-size: 0.9rem; line-height: 1.5;">Menganalisis karakteristik data secara visual. Membuat countplot distribusi target dan fitur kategori, histogram umur dan tinggi badan, boxplot hubungan fitur numerik terhadap status gizi, serta visualisasi heatmap korelasi pearson.</p>
        </div>
        <div class="glass-card" style="border-left: 5px solid #9B59B6;">
            <h4 style="margin: 0;">👤 Anggota 4 - Fahmi Syarief H. (2301010003)</h4>
            <p style="font-size: 0.85rem; font-weight: bold; text-transform: uppercase; margin: 3px 0;">Model Training Awal</p>
            <p style="font-size: 0.9rem; line-height: 1.5;">Bertanggung jawab dalam melatih model dasar (baseline) sebelum dilakukan optimasi. Algoritma yang dilatih meliputi Logistic Regression, Decision Tree Classifier, dan Random Forest Classifier pada data latihan hasil SMOTE.</p>
        </div>
        <div class="glass-card" style="border-left: 5px solid #F39C12;">
            <h4 style="margin: 0;">👤 Anggota 5 - Made Arya Sutha (2301010030)</h4>
            <p style="font-size: 0.85rem; font-weight: bold; text-transform: uppercase; margin: 3px 0;">Hyperparameter Tuning, Ensemble & Evaluation</p>
            <p style="font-size: 0.9rem; line-height: 1.5;">Mengoptimasi model dengan GridSearchCV, melatih model ensemble (AdaBoost & Voting Classifier), menyusun tabel perbandingan performa, memplot confusion matrix, mengarahkan analisis Feature Importance, serta mengekspor objek model terpilih.</p>
        </div>
        <div class="glass-card" style="border-left: 5px solid #1ABC9C;">
            <h4 style="margin: 0;">👤 Anggota 6 - Ahmad Jul Hadi (2301010019)</h4>
            <p style="font-size: 0.85rem; font-weight: bold; text-transform: uppercase; margin: 3px 0 10px 0;">Deployment Streamlit</p>
            <p style="font-size: 0.9rem; line-height: 1.5;">Melakukan refactoring kode notebook ke dalam struktur file Python modular, mengintegrasikan visualisasi Plotly interaktif, membuat dashboard prediksi beserta gauge chart dan merilis sistem ke server web cloud.</p>
        </div>
        <!-- Kartu placeholder untuk melengkapi grid 2x4 -->
        <div class="glass-card" style="border-left: 5px solid transparent; visibility: hidden;"></div>
        <div class="glass-card" style="border-left: 5px solid transparent; visibility: hidden;"></div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
