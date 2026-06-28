import streamlit as st
import os
from utils.loader import load_model, load_dataset
from preprocessing.preprocessing import preprocess

def main():
    st.markdown('<h1 style="color: #FFFFFF; font-weight: 800; text-align; font-size: 2.2rem;">PREDIKSI STATUS GIZI DAN RISIKO STUNTING BALITA MENGGUNAKAN MACHINE LEARNING</h1>', unsafe_allow_html=True)
    st.write("---")

    # Tampilkan Gambar Banner
    banner_path = os.path.join("assets", "banner.png")
    if os.path.exists(banner_path):
        st.image(banner_path, use_container_width=True)

    # Muat data dan detail model secara dinamis
    try:
        df_raw = load_dataset()
        df = preprocess(df_raw)
        
        num_rows = df.shape[0] # akan bernilai 120.999
        num_cols = df.shape[1]
        best_model_name = "Random Forest"
    except Exception as e:
        num_rows = 120999
        num_cols = 4
        best_model_name = "Random Forest"
        st.sidebar.warning(f"Error memuat metrik awal: {e}")

    # Tata Letak: Kartu Ringkasan
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="glass-card" style="text-align: center;">'
            f'<p style="color: #FFFFFF; margin-bottom: 5px; font-weight: 600; text-transform: uppercase; font-size: 0.85rem;">Jumlah Sampel Data</p>'
            f'<h2 style="color: #FFFFFF; margin: 0; font-size: 2.2rem; font-weight: 800;">{num_rows:,}</h2>'
            f'<span style="color: #2ECC71; font-size: 0.85rem; font-weight: 600;">Balita terdata</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'<div class="glass-card" style="text-align: center;">'
            f'<p style="color: #FFFFFF; margin-bottom: 5px; font-weight: 600; text-transform: uppercase; font-size: 0.85rem;">Jumlah Fitur Utama</p>'
            f'<h2 style="color: #FFFFFF; margin: 0; font-size: 2.2rem; font-weight: 800;">{num_cols - 1} Fitur</h2>'
            f'<span style="color: #3498DB; font-size: 0.85rem; font-weight: 600;">+ 1 Target Gizi</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f'<div class="glass-card" style="text-align: center;">'
            f'<p style="color: #FFFFFF; margin-bottom: 5px; font-weight: 600; text-transform: uppercase; font-size: 0.85rem;">Model Terbaik (F1-Macro)</p>'
            f'<h2 style="color: #FFFFFF; margin: 0; font-size: 1.8rem; font-weight: 800; min-height: 50px; display: flex; align-items: center; justify-content: center;">{best_model_name}</h2>'
            f'<span style="color: #8E44AD; font-size: 0.85rem; font-weight: 600;">Selected Best Estimator</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    # Tab Konten Halaman Beranda
    tab_desc, tab_goal, tab_features = st.tabs([
        "📖 Deskripsi Penelitian", 
        "🎯 Tujuan Penelitian", 
        "📋 Keterangan Fitur"
    ])
    
    with tab_desc:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #FFFFFF;">Latar Belakang Proyek</h3>
            <p style="line-height: 1.6; color: #FFFFFF;">
                Stunting merupakan kondisi kegagalan pertumbuhan pada anak (pertumbuhan tubuh dan otak) akibat kekurangan gizi dalam waktu yang lama. 
                Hal ini menyebabkan anak menjadi lebih pendek dari tinggi badan rata-rata anak seusianya dan memiliki keterlambatan berpikir. 
                Penelitian ini dikembangkan untuk melakukan deteksi dini risiko stunting dan pengelompokan status gizi anak balita berdasarkan 
                variabel fisik dan usia dengan pendekatan disiplin ilmu <strong>Data Mining</strong> dan <strong>Machine Learning</strong>.
            </p>
            <p style="line-height: 1.6; color: #FFFFFF;">
                Dengan memanfaatkan data fisik balita, model pembelajaran mesin dapat memberikan estimasi klasifikasi gizi 
                (Normal, Stunted, Severely Stunted, Tinggi) secara akurat dan objektif, yang diharapkan mampu menjadi alat bantu 
                penapisan (screening) bagi posyandu maupun institusi kesehatan masyarakat.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with tab_goal:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #FFFFFF;">Tujuan Penelitian</h3>
            <ol style="line-height: 1.8; color: #FFFFFF;">
                <li><strong>Deteksi Dini Stunting:</strong> Membangun sistem yang mampu mendeteksi tingkat keparahan risiko stunting (Normal, Pendek, Sangat Pendek) sejak dini.</li>
                <li><strong>Optimalisasi Kebijakan Gizi:</strong> Menyediakan data klasifikasi gizi balita yang valid guna menunjang penargetan bantuan pangan dan suplemen yang efektif.</li>
                <li><strong>Perbandingan Algoritma:</strong> Menganalisis akurasi algoritma klasifikasi <em>Logistic Regression</em>, <em>Decision Tree</em>, <em>Random Forest</em>, serta teknik ensemble (<em>AdaBoost</em> dan <em>Voting Classifier</em>) untuk mencari performa terbaik.</li>
                <li><strong>Alat Bantu Digital:</strong> Menyediakan aplikasi kalkulator gizi berbasis web (Streamlit) yang interaktif, mudah digunakan oleh kader Posyandu, dan siap dideploy ke awan.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
    with tab_features:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #FFFFFF;">Deskripsi Fitur Dataset</h3>
            <p style="color: #FFFFFF;">Dataset yang digunakan memiliki 4 kolom utama:</p>
            <table style="width: 100%; border-collapse: collapse; margin-top: 10px; color: #FFFFFF;">
                <thead>
                    <tr style="border-bottom: 2px solid rgba(255, 255, 255, 0.2); text-align: left; font-weight: bold;">
                        <th style="padding: 10px; color: #FFFFFF;">Nama Fitur</th>
                        <th style="padding: 10px; color: #FFFFFF;">Tipe Data</th>
                        <th style="padding: 10px; color: #FFFFFF;">Deskripsi</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
                        <td style="padding: 10px; font-weight: 600; color: #FFFFFF;">Umur (bulan)</td>
                        <td style="padding: 10px; font-family: monospace; color: #FFFFFF;">Integer</td>
                        <td style="padding: 10px; color: #FFFFFF;">Usia balita saat pengukuran (rentang: 0 hingga 60 bulan).</td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
                        <td style="padding: 10px; font-weight: 600; color: #FFFFFF;">Jenis Kelamin</td>
                        <td style="padding: 10px; font-family: monospace; color: #FFFFFF;">Categorical</td>
                        <td style="padding: 10px; color: #FFFFFF;">Jenis kelamin balita (Laki-laki atau Perempuan).</td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
                        <td style="padding: 10px; font-weight: 600; color: #FFFFFF;">Tinggi Badan (cm)</td>
                        <td style="padding: 10px; font-family: monospace; color: #FFFFFF;">Float</td>
                        <td style="padding: 10px; color: #FFFFFF;">Tinggi badan balita dalam satuan sentimeter (rentang: 40 hingga 130 cm).</td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
                        <td style="padding: 10px; font-weight: 600; color: #FFFFFF;">Status Gizi (Target)</td>
                        <td style="padding: 10px; font-family: monospace; color: #FFFFFF;">Categorical</td>
                        <td style="padding: 10px; color: #FFFFFF;">Label target status gizi: <strong>Severely Stunted</strong>, <strong>Stunted</strong>, <strong>Normal</strong>, atau <strong>Tinggi</strong>.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
