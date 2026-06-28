import os
import tempfile
import base64
import datetime
import matplotlib
matplotlib.use('Agg') # Backend headless untuk keamanan thread di server web
import matplotlib.pyplot as plt
from fpdf import FPDF

# Warna dinamis yang mencerminkan tingkat keparahan klinis
COLOR_MAP = {
    'normal': '#2ECC71',
    'stunted': '#F39C12',
    'severely stunted': '#E74C3C',
    'tinggi': '#3498DB'
}

def generate_confidence_meter(confidence_pct, filepath):
    """
    Menghasilkan progress bar horizontal yang bersih untuk menunjukkan tingkat kepercayaan prediksi.
    """
    fig, ax = plt.subplots(figsize=(6, 1.0))
    
    # Gambar jalur latar belakang
    ax.barh([0], [100], color='#EAEDED', height=0.4, align='center')
    
    # Tentukan warna berdasarkan nilai confidence
    color = '#E74C3C' # Merah
    if confidence_pct >= 80:
        color = '#2ECC71' # Hijau
    elif confidence_pct >= 50:
        color = '#F39C12' # Kuning/Oranye
        
    # Gambar batang nilai confidence
    ax.barh([0], [confidence_pct], color=color, height=0.4, align='center')
    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_xlabel('Confidence Score (%)', fontsize=8, fontweight='bold')
    ax.set_title(f'Prediction Confidence: {confidence_pct:.2f}%', fontsize=9, fontweight='bold', pad=4)
    
    # Hapus semua garis bingkai (spines)
    for spine in ax.spines.values():
        spine.set_visible(False)
        
    plt.tight_layout()
    plt.savefig(filepath, dpi=200)
    plt.close()

def generate_probability_bar_chart(probs_dict, filepath):
    """
    Menghasilkan grafik batang horizontal yang menampilkan distribusi probabilitas tiap kelas.
    """
    classes = list(probs_dict.keys())
    values = list(probs_dict.values())
    
    # Ubah ke Title Case untuk tampilan
    classes_title = [c.title() for c in classes]
    
    # Pemetaan warna berdasarkan kelas
    colors = []
    for c in classes:
        c_lower = c.lower()
        if 'normal' in c_lower:
            colors.append('#2ECC71')
        elif 'severely' in c_lower:
            colors.append('#E74C3C')
        elif 'stunted' in c_lower:
            colors.append('#F39C12')
        else:
            colors.append('#3498DB')
            
    fig, ax = plt.subplots(figsize=(5.5, 2.5))
    bars = ax.barh(classes_title, values, color=colors, height=0.6, edgecolor='none')
    ax.set_xlim(0, 110)
    ax.set_xlabel('Probabilitas (%)', fontsize=8, fontweight='bold')
    ax.set_title('Distribusi Probabilitas Kelas', fontsize=9, fontweight='bold', pad=8)
    
    # Tambahkan label nilai pada setiap batang
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1.5, bar.get_y() + bar.get_height()/2, f'{width:.2f}%', 
                va='center', ha='left', fontsize=7.5, fontweight='bold')
                
    # Hapus garis bingkai atas dan kanan
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
        
    plt.tight_layout()
    plt.savefig(filepath, dpi=200)
    plt.close()

def generate_probability_pie_chart(probs_dict, filepath):
    """
    Menghasilkan grafik pie komposisi probabilitas prediksi.
    """
    classes = list(probs_dict.keys())
    values = list(probs_dict.values())
    
    # Filter kelas dengan probabilitas yang signifikan (>= 0.5%)
    non_zero = [(c.title(), v) for c, v in zip(classes, values) if v >= 0.5]
    if not non_zero:
        non_zero = [(c.title(), v) for c, v in zip(classes, values)]
        
    lbls, vals = zip(*non_zero)
    
    colors_map = {
        'Normal': '#2ECC71',
        'Stunted': '#F39C12',
        'Severely Stunted': '#E74C3C',
        'Tinggi': '#3498DB'
    }
    colors = [colors_map.get(lbl, '#95A5A6') for lbl in lbls]
    
    fig, ax = plt.subplots(figsize=(3.5, 2.5))
    wedges, texts, autotexts = ax.pie(
        vals, 
        labels=lbls, 
        autopct='%1.1f%%', 
        colors=colors, 
        startangle=140, 
        textprops={'fontsize': 7.5}
    )
    # Tebalkan label persentase
    for autotext in autotexts:
        autotext.set_fontweight('bold')
        
    ax.axis('equal')
    ax.set_title('Komposisi Probabilitas', fontsize=9, fontweight='bold', pad=8)
    
    plt.tight_layout()
    plt.savefig(filepath, dpi=200)
    plt.close()

class PDFReport(FPDF):
    def header(self):
        # Gambar band header pada halaman pertama
        if self.page_no() == 1:
            # Tampilkan logo jika file tersedia
            logo_path = os.path.join("assets", "logo.png")
            if os.path.exists(logo_path):
                self.image(logo_path, x=10, y=8, w=15)
                self.set_x(28)
            else:
                self.set_x(10)
                
            self.set_font('helvetica', 'B', 14)
            self.cell(0, 6, 'LAPORAN DETEKSI STATUS GIZI BALITA', ln=True, align='L')
            self.set_font('helvetica', 'I', 8.5)
            self.cell(0, 4, 'Sistem Deteksi Tumbuh Kembang & Risiko Stunting - UAS Data Mining Lanjut', ln=True, align='L')
            self.ln(5)
            # Garis pembatas tipis
            self.line(10, 26, 200, 26)
            self.ln(6)
            
    def footer(self):
        # Posisi 1.5 cm dari bawah halaman
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f'Halaman {self.page_no()}/{{nb}}', align='C')
        self.cell(0, 10, 'Aplikasi Deteksi Stunting Balita', align='R')

def build_pdf_report(umur, gender, tinggi, status_gizi, confidence_pct, model_name, prediction_time, advice_text, probs_dict):
    """
    Membangun dan mengembalikan laporan PDF yang dihasilkan dalam format biner.
    """
    # Buat nama file sementara
    temp_dir = tempfile.gettempdir()
    gauge_path = os.path.join(temp_dir, f"gauge_{os.getpid()}.png")
    bar_path = os.path.join(temp_dir, f"bar_{os.getpid()}.png")
    pie_path = os.path.join(temp_dir, f"pie_{os.getpid()}.png")
    
    try:
        # 1. Hasilkan grafik statis menggunakan Matplotlib
        generate_confidence_meter(confidence_pct, gauge_path)
        generate_probability_bar_chart(probs_dict, bar_path)
        generate_probability_pie_chart(probs_dict, pie_path)
        
        # 2. Bangun Dokumen PDF
        pdf = PDFReport(orientation='P', unit='mm', format='A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_margins(10, 10, 10)
        
        # Seksi 1: Parameter & Hasil Prediksi
        pdf.set_font('helvetica', 'B', 11)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 7, '1. PARAMETER PENGUKURAN & HASIL PREDIKSI', ln=True)
        pdf.ln(1)
        
        # Tabel grid parameter
        pdf.set_fill_color(245, 247, 250)
        pdf.set_font('helvetica', 'B', 9.5)
        pdf.cell(95, 7.5, ' Parameter / Metrik Analisis', border=1, fill=True)
        pdf.cell(95, 7.5, ' Nilai Hasil Pengukuran', border=1, ln=True, fill=True)
        
        pdf.set_font('helvetica', '', 9)
        pdf.cell(95, 6.5, ' Umur Balita', border=1)
        pdf.cell(95, 6.5, f' {umur} Bulan', border=1, ln=True)
        
        pdf.cell(95, 6.5, ' Jenis Kelamin', border=1)
        pdf.cell(95, 6.5, f' {gender.title()}', border=1, ln=True)
        
        pdf.cell(95, 6.5, ' Tinggi Badan', border=1)
        pdf.cell(95, 6.5, f' {tinggi:.1f} cm', border=1, ln=True)
        
        pdf.set_font('helvetica', 'B', 9)
        pdf.cell(95, 6.5, ' Status Gizi Terprediksi', border=1)
        # Highlight warna teks status berdasarkan tingkat keparahan
        status_label = status_gizi.title()
        pdf.cell(95, 6.5, f' {status_label}', border=1, ln=True)
        
        pdf.set_font('helvetica', '', 9)
        pdf.cell(95, 6.5, ' Confidence Score (%)', border=1)
        pdf.cell(95, 6.5, f' {confidence_pct:.2f}%', border=1, ln=True)
        
        pdf.cell(95, 6.5, ' Algoritma Model Terbaik', border=1)
        pdf.cell(95, 6.5, f' {model_name}', border=1, ln=True)
        
        pdf.cell(95, 6.5, ' Waktu Analisis Laporan', border=1)
        pdf.cell(95, 6.5, f' {prediction_time}', border=1, ln=True)
        pdf.ln(5)
        
        # Seksi 2: Blok Rekomendasi Klinis
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(0, 7, '2. HASIL DIAGNOSIS & REKOMENDASI MEDIS', ln=True)
        pdf.ln(1)
        
        # Gaya kotak peringatan berdasarkan tingkat keparahan
        status_lower = status_gizi.lower()
        if 'severely stunted' in status_lower:
            pdf.set_fill_color(254, 243, 243) # Merah muda
            pdf.set_text_color(176, 28, 28) # Teks merah
            border_color_rgb = (176, 28, 28)
        elif 'stunted' in status_lower:
            pdf.set_fill_color(255, 250, 240) # Oranye/kuning muda
            pdf.set_text_color(184, 97, 0) # Teks oranye
            border_color_rgb = (184, 97, 0)
        elif 'normal' in status_lower:
            pdf.set_fill_color(244, 251, 244) # Hijau muda
            pdf.set_text_color(21, 108, 51) # Teks hijau
            border_color_rgb = (21, 108, 51)
        else: # Tinggi
            pdf.set_fill_color(240, 248, 255) # Biru muda
            pdf.set_text_color(18, 93, 152) # Teks biru
            border_color_rgb = (18, 93, 152)
            
        pdf.set_font('helvetica', 'B', 9)
        pdf.cell(0, 6, f' Rekomendasi Status: {status_label}', border='TLR', ln=True, fill=True)
        pdf.set_font('helvetica', '', 9.5)
        
        # Wrapping multi-baris untuk teks rekomendasi
        pdf.multi_cell(0, 5.5, f' {advice_text}', border='BLR', fill=True)
        pdf.set_text_color(30, 30, 30) # reset warna teks
        pdf.ln(6)
        
        # Seksi 3: Grafik Visualisasi
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(0, 7, '3. GRAFIK ANALISIS PROBABILITAS PREDIKSI', ln=True)
        pdf.ln(1)
        
        # Sisipkan grafik Confidence Gauge
        if os.path.exists(gauge_path):
            pdf.image(gauge_path, x=15, w=180)
            pdf.ln(2)
            
        # Sisipkan grafik berdampingan
        y_pos = pdf.get_y()
        if os.path.exists(bar_path):
            pdf.image(bar_path, x=10, y=y_pos, w=100)
        if os.path.exists(pie_path):
            pdf.image(pie_path, x=115, y=y_pos, w=85)
            
        # Keluarkan PDF sebagai string biner
        pdf_str = pdf.output(dest='S')
        return pdf_str.encode('latin1')
        
    finally:
        # 3. Bersihkan file sementara
        for path in [gauge_path, bar_path, pie_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass
