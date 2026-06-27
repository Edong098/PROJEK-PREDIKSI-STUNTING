import os
import tempfile
import base64
import datetime
import matplotlib
matplotlib.use('Agg') # Headless backend for thread-safety in web servers
import matplotlib.pyplot as plt
from fpdf import FPDF

# Dynamic colors matching clinical severity
COLOR_MAP = {
    'normal': '#2ECC71',
    'stunted': '#F39C12',
    'severely stunted': '#E74C3C',
    'tinggi': '#3498DB'
}

def generate_confidence_meter(confidence_pct, filepath):
    """
    Generates a clean horizontal progress bar indicating prediction confidence.
    """
    fig, ax = plt.subplots(figsize=(6, 1.0))
    
    # Draw background track
    ax.barh([0], [100], color='#EAEDED', height=0.4, align='center')
    
    # Determine color
    color = '#E74C3C' # Red
    if confidence_pct >= 80:
        color = '#2ECC71' # Green
    elif confidence_pct >= 50:
        color = '#F39C12' # Yellow/Orange
        
    # Draw value bar
    ax.barh([0], [confidence_pct], color=color, height=0.4, align='center')
    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_xlabel('Confidence Score (%)', fontsize=8, fontweight='bold')
    ax.set_title(f'Prediction Confidence: {confidence_pct:.2f}%', fontsize=9, fontweight='bold', pad=4)
    
    # Remove all borders/spines
    for spine in ax.spines.values():
        spine.set_visible(False)
        
    plt.tight_layout()
    plt.savefig(filepath, dpi=200)
    plt.close()

def generate_probability_bar_chart(probs_dict, filepath):
    """
    Generates horizontal bar chart showing probability distribution of classes.
    """
    classes = list(probs_dict.keys())
    values = list(probs_dict.values())
    
    # Title-case for display
    classes_title = [c.title() for c in classes]
    
    # Color mapping
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
    
    # Add values on the bar
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1.5, bar.get_y() + bar.get_height()/2, f'{width:.2f}%', 
                va='center', ha='left', fontsize=7.5, fontweight='bold')
                
    # Remove top and right spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
        
    plt.tight_layout()
    plt.savefig(filepath, dpi=200)
    plt.close()

def generate_probability_pie_chart(probs_dict, filepath):
    """
    Generates a pie chart of prediction probabilities composition.
    """
    classes = list(probs_dict.keys())
    values = list(probs_dict.values())
    
    # Filter classes with meaningful probability (>= 0.5%)
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
    # Bold the percentage labels
    for autotext in autotexts:
        autotext.set_fontweight('bold')
        
    ax.axis('equal')
    ax.set_title('Komposisi Probabilitas', fontsize=9, fontweight='bold', pad=8)
    
    plt.tight_layout()
    plt.savefig(filepath, dpi=200)
    plt.close()

class PDFReport(FPDF):
    def header(self):
        # Draw a header band on page 1
        if self.page_no() == 1:
            # Draw logo if exists
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
            # Faint line divider
            self.line(10, 26, 200, 26)
            self.ln(6)
            
    def footer(self):
        # Position 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f'Halaman {self.page_no()}/{{nb}}', align='C')
        self.cell(0, 10, 'Aplikasi Deteksi Stunting Balita', align='R')

def build_pdf_report(umur, gender, tinggi, status_gizi, confidence_pct, model_name, prediction_time, advice_text, probs_dict):
    """
    Builds and returns the generated PDF report in binary format.
    """
    # Create temp filenames
    temp_dir = tempfile.gettempdir()
    gauge_path = os.path.join(temp_dir, f"gauge_{os.getpid()}.png")
    bar_path = os.path.join(temp_dir, f"bar_{os.getpid()}.png")
    pie_path = os.path.join(temp_dir, f"pie_{os.getpid()}.png")
    
    try:
        # 1. Generate Matplotlib static charts
        generate_confidence_meter(confidence_pct, gauge_path)
        generate_probability_bar_chart(probs_dict, bar_path)
        generate_probability_pie_chart(probs_dict, pie_path)
        
        # 2. Build PDF Document
        pdf = PDFReport(orientation='P', unit='mm', format='A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_margins(10, 10, 10)
        
        # Section 1: Parameter & Prediksi
        pdf.set_font('helvetica', 'B', 11)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 7, '1. PARAMETER PENGUKURAN & HASIL PREDIKSI', ln=True)
        pdf.ln(1)
        
        # Table Grid
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
        # Highlight predicted status text color based on severity
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
        
        # Section 2: Clinical Advice Block
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(0, 7, '2. HASIL DIAGNOSIS & REKOMENDASI MEDIS', ln=True)
        pdf.ln(1)
        
        # Style warning box based on severity
        status_lower = status_gizi.lower()
        if 'severely stunted' in status_lower:
            pdf.set_fill_color(254, 243, 243) # Light red
            pdf.set_text_color(176, 28, 28) # Red text
            border_color_rgb = (176, 28, 28)
        elif 'stunted' in status_lower:
            pdf.set_fill_color(255, 250, 240) # Light orange/yellow
            pdf.set_text_color(184, 97, 0) # Orange text
            border_color_rgb = (184, 97, 0)
        elif 'normal' in status_lower:
            pdf.set_fill_color(244, 251, 244) # Light green
            pdf.set_text_color(21, 108, 51) # Green text
            border_color_rgb = (21, 108, 51)
        else: # Tinggi
            pdf.set_fill_color(240, 248, 255) # Light blue
            pdf.set_text_color(18, 93, 152) # Blue text
            border_color_rgb = (18, 93, 152)
            
        pdf.set_font('helvetica', 'B', 9)
        pdf.cell(0, 6, f' Rekomendasi Status: {status_label}', border='TLR', ln=True, fill=True)
        pdf.set_font('helvetica', '', 9.5)
        
        # Multicell wrapping for recommendations
        pdf.multi_cell(0, 5.5, f' {advice_text}', border='BLR', fill=True)
        pdf.set_text_color(30, 30, 30) # reset
        pdf.ln(6)
        
        # Section 3: Visualizations
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(0, 7, '3. GRAFIK ANALISIS PROBABILITAS PREDIKSI', ln=True)
        pdf.ln(1)
        
        # Embed Confidence Gauge
        if os.path.exists(gauge_path):
            pdf.image(gauge_path, x=15, w=180)
            pdf.ln(2)
            
        # Embed side-by-side charts
        y_pos = pdf.get_y()
        if os.path.exists(bar_path):
            pdf.image(bar_path, x=10, y=y_pos, w=100)
        if os.path.exists(pie_path):
            pdf.image(pie_path, x=115, y=y_pos, w=85)
            
        # Output PDF as byte string
        pdf_str = pdf.output(dest='S')
        return pdf_str.encode('latin1')
        
    finally:
        # 3. Clean up temporary files
        for path in [gauge_path, bar_path, pie_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass
