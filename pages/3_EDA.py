import streamlit as st
import importlib
import utils.visualization
importlib.reload(utils.visualization)
from utils.loader import load_dataset
from preprocessing.preprocessing import preprocess
from utils.visualization import (
    plot_target_distribution,
    plot_gender_distribution,
    plot_age_distribution,
    plot_height_distribution,
    plot_correlation_heatmap,
    plot_boxplot_age,
    plot_boxplot_height,
    plot_scatterplot
)

def main():
    st.markdown('<h1 class="gradient-text" style="font-size: 2.8rem; margin-bottom: 0px;">EXPLORATORY DATA ANALYSIS</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-top: 5px; color: #FFFFFF; font-weight: 500;">Visualisasi Hubungan Fitur Fisik dan Status Gizi Balita</h3>', unsafe_allow_html=True)
    st.write("---")

    # Muat dan bersihkan dataset untuk keperluan EDA
    with st.spinner("Memproses visualisasi data..."):
        try:
            df_raw = load_dataset()
            df_clean = preprocess(df_raw)
        except Exception as e:
            st.error(f"Gagal memuat visualisasi: {e}")
            return

    # Tab untuk berbagai jenis analisis
    tab_dist, tab_box, tab_corr = st.tabs([
        "📊 Distribusi Frekuensi", 
        "📦 Boxplot & Hubungan", 
        "🔥 Heatmap Korelasi"
    ])

    with tab_dist:
        st.markdown("### 1. Distribusi Kelas Target dan Fitur Kategorikal")
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = plot_target_distribution(df_clean)
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown(
                '<div class="glass-card" style="margin-top: 10px; border-top: 3px solid #2ECC71;">'
                '<h5>💡 Distribusi Status Gizi:</h5>'
                '<p style="font-size: 0.85rem; color: #FFFFFF; line-height: 1.5; margin: 0;">'
                'Grafik di atas menunjukkan dominasi kelas <strong>Normal</strong> dibandingkan kelas lainnya. '
                'Ini mengindikasikan adanya masalah ketidakseimbangan kelas (imbalance data). Kelas <strong>Severely Stunted</strong> '
                'dan <strong>Stunted</strong> merupakan kelompok minoritas berisiko tinggi. Ketidakseimbangan ini diatasi dengan '
                'teknik <strong>SMOTE</strong> pada tahap prapemrosesan sebelum data dimasukkan ke dalam model ML guna mencegah '
                'model bias terhadap kelas Normal.'
                '</p>'
                '</div>', 
                unsafe_allow_html=True
            )
            
        with col2:
            fig2 = plot_gender_distribution(df_clean)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown(
                '<div class="glass-card" style="margin-top: 10px; border-top: 3px solid #3498DB;">'
                '<h5>💡 Distribusi Jenis Kelamin:</h5>'
                '<p style="font-size: 0.85rem; color: #FFFFFF; line-height: 1.5; margin: 0;">'
                'Proporsi balita berjenis kelamin <strong>Laki-laki</strong> dan <strong>Perempuan</strong> di dalam dataset '
                'terbagi secara seimbang dengan rasio mendekati 50:50. Hal ini menjamin bahwa model pembelajaran mesin yang dilatih '
                'tidak memiliki kecenderungan bias gender dalam memprediksi status stunting balita.'
                '</p>'
                '</div>', 
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("### 2. Distribusi Fitur Numerik Kontinu")
        col3, col4 = st.columns(2)
        
        with col3:
            fig3 = plot_age_distribution(df_clean)
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown(
                '<div class="glass-card" style="margin-top: 10px;">'
                '<h5>💡 Distribusi Umur:</h5>'
                '<p style="font-size: 0.85rem; color: #FFFFFF; line-height: 1.5; margin: 0;">'
                'Distribusi umur balita menunjukkan persebaran yang relatif merata di seluruh rentang usia balita (0 hingga 60 bulan). '
                'Adanya fluktuasi kecil di beberapa kelompok usia adalah hal yang wajar dalam pengambilan sampel acak populasi balita.'
                '</p>'
                '</div>', 
                unsafe_allow_html=True
            )
            
        with col4:
            fig4 = plot_height_distribution(df_clean)
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown(
                '<div class="glass-card" style="margin-top: 10px;">'
                '<h5>💡 Distribusi Tinggi Badan:</h5>'
                '<p style="font-size: 0.85rem; color: #FFFFFF; line-height: 1.5; margin: 0;">'
                'Kurva tinggi badan balita mengikuti bentuk distribusi normal (bell-curve). Mayoritas balita terkonsentrasi pada '
                'rentang tinggi badan 60 cm s.d. 100 cm. Data pencilan (outliers) di bawah 40 cm or di atas 130 cm telah dibersihkan '
                'pada proses prapemrosesan (data cleaning) berbasis IQR.'
                '</p>'
                '</div>', 
                unsafe_allow_html=True
            )

    with tab_box:
        st.markdown("### 3. Analisis Hubungan Fitur Fisik terhadap Kategori Gizi")
        st.write("Visualisasi Boxplot membantu mengamati rentang nilai kuartil (Q1, Q2, Q3) serta sebaran data umur dan tinggi badan di setiap kelas gizi.")
        
        col5, col6 = st.columns(2)
        with col5:
            fig5 = plot_boxplot_age(df_clean)
            st.plotly_chart(fig5, use_container_width=True)
            st.markdown(
                '<div class="glass-card" style="margin-top: 10px;">'
                '<h5>💡 Boxplot Umur vs Status Gizi:</h5>'
                '<p style="font-size: 0.85rem; color: #FFFFFF; line-height: 1.5; margin: 0;">'
                'Median umur (garis tengah box) untuk kategori gizi <strong>normal</strong> cenderung lebih rendah dibandingkan kategori <strong>stunted</strong> dan <strong>severely stunted</strong>. '
                'Ini memberikan gambaran klinis bahwa stunting kronis sering kali baru terdeteksi atau menumpuk seiring bertambahnya usia balita (24-60 bulan) '
                'akibat defisit nutrisi yang terakumulasi dalam jangka panjang.'
                '</p>'
                '</div>', 
                unsafe_allow_html=True
            )
            
        with col6:
            fig6 = plot_boxplot_height(df_clean)
            st.plotly_chart(fig6, use_container_width=True)
            st.markdown(
                '<div class="glass-card" style="margin-top: 10px;">'
                '<h5>💡 Boxplot Tinggi vs Status Gizi:</h5>'
                '<p style="font-size: 0.85rem; color: #FFFFFF; line-height: 1.5; margin: 0;">'
                'Tinggi badan memiliki perbedaan median yang sangat tajam di antara setiap kategori. Balita dengan status <strong>Severely Stunted</strong> '
                'memiliki rentang tinggi badan terendah (berada di bawah), disusul oleh <strong>Stunted</strong>, lalu <strong>Normal</strong>, dan tertinggi dipegang oleh kategori <strong>Tinggi</strong>. '
                'Ini mengonfirmasi secara kuat bahwa tinggi badan merupakan pembeda utama dalam penentuan target status gizi.'
                '</p>'
                '</div>', 
                unsafe_allow_html=True
            )
            
        st.markdown("---")
        st.markdown("### 4. Scatterplot Korelasi Multi-Variabel")
        fig7 = plot_scatterplot(df_clean)
        st.plotly_chart(fig7, use_container_width=True)
        st.markdown(
            '<div class="glass-card" style="margin-top: 10px; border-left: 5px solid #F39C12;">'
            '<h5>💡 Hubungan Umur, Tinggi Badan, dan Status Gizi:</h5>'
            '<p style="font-size: 0.875rem; color: #FFFFFF; line-height: 1.6; margin: 0;">'
            'Grafik sebar di atas menunjukkan batas-batas linier non-parametrik yang jelas dalam klasifikasi stunting:<br>'
            '• <strong>Warna Merah (Severely Stunted):</strong> Terkonsentrasi di bagian paling bawah kurva, menunjukkan tinggi badan yang sangat kurang dari standar umur tumbuh kembangnya.<br>'
            '• <strong>Warna Jingga (Stunted):</strong> Membentuk lapisan pembatas di atas kelas severely stunted.<br>'
            '• <strong>Warna Hijau (Normal):</strong> Menempati area bagian tengah kurva yang paling padat, menunjukkan tinggi badan proporsional dengan umurnya.<br>'
            '• <strong>Warna Biru (Tinggi):</strong> Berada di bagian paling atas kurva, menunjukkan anak dengan tinggi badan di atas rata-rata kelompok usianya.'
            '</p>'
            '</div>', 
            unsafe_allow_html=True
        )

    with tab_corr:
        st.markdown("### 5. Heatmap Korelasi Pearson")
        st.write("Menampilkan koefisien korelasi linear untuk mengukur seberapa erat hubungan antar variabel.")
        
        col_c1, col_c2 = st.columns([2, 1])
        with col_c1:
            fig8 = plot_correlation_heatmap(df_clean)
            st.plotly_chart(fig8, use_container_width=True)
        with col_c2:
            st.markdown(
                '<div class="glass-card" style="margin-top: 40px; height: 90%;">'
                '<h5>💡 Matriks Korelasi:</h5>'
                '<p style="font-size: 0.85rem; color: #FFFFFF; line-height: 1.6; margin: 0;">'
                '• <strong>Korelasi Umur vs Tinggi Badan (0.79):</strong> Memiliki nilai positif yang sangat kuat mendekati +1.0. Menunjukkan hubungan linier langsung di mana pertambahan umur anak diikuti dengan pertambahan tinggi badan.<br>'
                '• <strong>Korelasi Gender (-0.03):</strong> Bernilai sangat mendekati 0, menandakan jenis kelamin tidak memiliki hubungan linear langsung terhadap status gizi anak.<br>'
                '• <strong>Status Gizi (Status_Encoded):</strong> Karena penentuan status gizi balita ditentukan secara komparatif non-linear (tinggi badan dibagi standar umur), korelasi linier sederhana memiliki nilai rendah. Di sinilah model machine learning non-linear seperti Decision Tree dan Random Forest bekerja sangat baik untuk menangkap interaksi non-linear tersebut.'
                '</p>'
                '</div>',
                unsafe_allow_html=True
            )

if __name__ == '__main__':
    main()
