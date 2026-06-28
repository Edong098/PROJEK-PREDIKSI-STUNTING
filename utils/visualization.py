# pyrefly: ignore [missing-import]
import plotly.express as px
# pyrefly: ignore [missing-import]
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Palet warna premium yang sesuai dengan tingkat keparahan klinis: Hijau, Kuning, Merah, dan Biru.
COLOR_MAP = {
    'normal': '#2ECC71',
    'stunted': '#F39C12',
    'severely stunted': '#E74C3C',
    'tinggi': '#3498DB'
}

GENDER_MAP = {
    'laki-laki': '#3498DB',
    'perempuan': '#E84393'
}

def apply_dark_theme(fig, height=350):
    """
    Menerapkan gaya tema gelap yang seragam ke semua figur Plotly.
    """
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', family="Outfit, Inter, sans-serif"),
        height=height,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.08)',
            zerolinecolor='rgba(255, 255, 255, 0.15)',
            tickfont=dict(color='#FFFFFF'),
            title=dict(font=dict(color='#FFFFFF'))
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.08)',
            zerolinecolor='rgba(255, 255, 255, 0.15)',
            tickfont=dict(color='#FFFFFF'),
            title=dict(font=dict(color='#FFFFFF'))
        )
    )
    return fig

# --- GRAFIK HALAMAN EDA ---

def plot_target_distribution(df):
    """
    Menampilkan grafik batang jumlah balita per kategori status gizi (Target).
    """
    counts = df['Status Gizi'].value_counts().reset_index()
    counts.columns = ['Status Gizi', 'Jumlah']
    
    fig = px.bar(
        counts, 
        x='Status Gizi', 
        y='Jumlah',
        color='Status Gizi',
        color_discrete_map=COLOR_MAP,
        title='Distribusi Status Gizi Balita',
        text='Jumlah'
    )
    fig = apply_dark_theme(fig)
    fig.update_layout(showlegend=False)
    fig.update_traces(textposition='outside', textfont=dict(color='#FFFFFF'))
    return fig

def plot_gender_distribution(df):
    """
    Menampilkan grafik batang jumlah balita per jenis kelamin.
    """
    counts = df['Jenis Kelamin'].value_counts().reset_index()
    counts.columns = ['Jenis Kelamin', 'Jumlah']
    
    fig = px.bar(
        counts, 
        x='Jenis Kelamin', 
        y='Jumlah',
        color='Jenis Kelamin',
        color_discrete_map=GENDER_MAP,
        title='Distribusi Jenis Kelamin Balita',
        text='Jumlah'
    )
    fig = apply_dark_theme(fig)
    fig.update_layout(showlegend=False)
    fig.update_traces(textposition='outside', textfont=dict(color='#FFFFFF'))
    return fig

def plot_age_distribution(df):
    """
    Menampilkan histogram distribusi umur balita.
    """
    fig = px.histogram(
        df, 
        x='Umur (bulan)', 
        nbins=20,
        title='Distribusi Umur Balita (Bulan)',
        color_discrete_sequence=['#2ECC71']
    )
    fig = apply_dark_theme(fig)
    fig.update_layout(bargap=0.1)
    return fig

def plot_height_distribution(df):
    """
    Menampilkan histogram distribusi tinggi badan balita.
    """
    fig = px.histogram(
        df, 
        x='Tinggi Badan (cm)', 
        nbins=25,
        title='Distribusi Tinggi Badan Balita (cm)',
        color_discrete_sequence=['#3498DB']
    )
    fig = apply_dark_theme(fig)
    fig.update_layout(bargap=0.1)
    return fig

def plot_correlation_heatmap(df):
    """
    Menghasilkan heatmap matriks korelasi antar variabel.
    """
    df_corr = df.copy()
    if 'Jenis Kelamin' in df_corr.columns:
        df_corr['Gender_Encoded'] = df_corr['Jenis Kelamin'].map({'perempuan': 0, 'laki-laki': 1})
    if 'Status Gizi' in df_corr.columns:
        valid_status = ['normal', 'stunted', 'severely stunted', 'tinggi']
        df_corr['Status_Encoded'] = df_corr['Status Gizi'].map({label: idx for idx, label in enumerate(valid_status)})
        
    cols = [col for col in ['Umur (bulan)', 'Tinggi Badan (cm)', 'Gender_Encoded', 'Status_Encoded'] if col in df_corr.columns]
    corr = df_corr[cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.index,
        colorscale='Viridis',
        zmin=-1, zmax=1,
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        showscale=True
    ))
    
    fig = apply_dark_theme(fig, height=400)
    fig.update_layout(
        title='Heatmap Korelasi Antar Fitur',
        margin=dict(l=60, r=40, t=60, b=60)
    )
    return fig

def plot_boxplot_age(df):
    """
    Menampilkan boxplot Umur vs Status Gizi.
    """
    valid_status = ['normal', 'stunted', 'severely stunted', 'tinggi']
    df_filtered = df[df['Status Gizi'].isin(valid_status)]
    
    fig = px.box(
        df_filtered, 
        x='Status Gizi', 
        y='Umur (bulan)',
        color='Status Gizi',
        color_discrete_map=COLOR_MAP,
        title='Umur vs Status Gizi',
        category_orders={'Status Gizi': valid_status}
    )
    fig = apply_dark_theme(fig)
    fig.update_layout(showlegend=False)
    return fig

def plot_boxplot_height(df):
    """
    Menampilkan boxplot Tinggi Badan vs Status Gizi.
    """
    valid_status = ['normal', 'stunted', 'severely stunted', 'tinggi']
    df_filtered = df[df['Status Gizi'].isin(valid_status)]
    
    fig = px.box(
        df_filtered, 
        x='Status Gizi', 
        y='Tinggi Badan (cm)',
        color='Status Gizi',
        color_discrete_map=COLOR_MAP,
        title='Tinggi Badan vs Status Gizi',
        category_orders={'Status Gizi': valid_status}
    )
    fig = apply_dark_theme(fig)
    fig.update_layout(showlegend=False)
    return fig

def plot_scatterplot(df):
    """
    Scatterplot yang menampilkan hubungan antara umur dan tinggi badan yang dikelompokkan berdasarkan status gizi.
    """
    valid_status = ['normal', 'stunted', 'severely stunted', 'tinggi']
    df_filtered = df[df['Status Gizi'].isin(valid_status)]
    
    if len(df_filtered) > 3000:
        df_sample = df_filtered.sample(n=3000, random_state=42)
    else:
        df_sample = df_filtered
        
    fig = px.scatter(
        df_sample, 
        x='Umur (bulan)', 
        y='Tinggi Badan (cm)',
        color='Status Gizi',
        color_discrete_map=COLOR_MAP,
        title='Hubungan Umur, Tinggi Badan, dan Status Gizi (Sampel 3,000 Data)',
        opacity=0.6,
        category_orders={'Status Gizi': valid_status}
    )
    fig = apply_dark_theme(fig, height=400)
    return fig


# --- GRAFIK HALAMAN MODEL ---

def plot_confusion_matrix(cm, classes, title="Confusion Matrix"):
    """
    Menampilkan confusion matrix dalam bentuk grafik heatmap.
    """
    cm_array = np.array(cm)
    cm_sum = cm_array.sum(axis=1)[:, np.newaxis]
    cm_pct = np.nan_to_num(np.round(100.0 * cm_array / cm_sum, 1))
    
    annotations = []
    for i, row in enumerate(cm):
        for j, val in enumerate(row):
            annotations.append(dict(
                x=classes[j],
                y=classes[i],
                text=f"<b>{val}</b><br>({cm_pct[i][j]}%)",
                showarrow=False,
                font=dict(color="white")
            ))
            
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=classes,
        y=classes,
        colorscale='Viridis',
        showscale=True
    ))
    
    fig = apply_dark_theme(fig, height=400)
    fig.update_layout(
        title=title,
        xaxis=dict(title='Prediksi', tickmode='array', tickvals=classes),
        yaxis=dict(title='Aktual', tickmode='array', tickvals=classes, autorange="reversed"),
        annotations=annotations,
        margin=dict(l=60, r=40, t=60, b=60)
    )
    return fig

def plot_feature_importance(importance_dict):
    """
    Menampilkan grafik batang horizontal untuk feature importances model Random Forest.
    """
    df_imp = pd.DataFrame(list(importance_dict.items()), columns=['Fitur', 'Importance'])
    df_imp = df_imp.sort_values(by='Importance', ascending=True)
    
    fig = px.bar(
        df_imp, 
        x='Importance', 
        y='Fitur',
        orientation='h',
        title='Feature Importance Model Random Forest',
        color='Importance',
        color_continuous_scale='Viridis'
    )
    fig = apply_dark_theme(fig, height=300)
    fig.update_layout(coloraxis_showscale=False)
    return fig


# --- GRAFIK DASHBOARD HALAMAN PREDIKSI ---

def plot_confidence_gauge(confidence_pct):
    """
    Menampilkan gauge melingkar modern yang menunjukkan tingkat kepercayaan prediksi.
    """
    gauge_color = "#E74C3C" # Merah
    if confidence_pct >= 80:
        gauge_color = "#2ECC71" # Hijau
    elif confidence_pct >= 50:
        gauge_color = "#F39C12" # Kuning/Oranye
        
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = confidence_pct,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Confidence Score (%)", 'font': {'size': 20, 'family': "Outfit, Inter, sans-serif", 'color': '#FFFFFF'}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#FFFFFF", 'tickfont': {'color': '#FFFFFF'}},
            'bar': {'color': gauge_color},
            'bgcolor': "rgba(255, 255, 255, 0.1)",
            'borderwidth': 2,
            'bordercolor': "rgba(255, 255, 255, 0.2)",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(231, 76, 60, 0.05)'},
                {'range': [50, 80], 'color': 'rgba(243, 156, 18, 0.05)'},
                {'range': [80, 100], 'color': 'rgba(46, 204, 113, 0.05)'}
            ]
        }
    ))
    
    fig = apply_dark_theme(fig, height=300)
    fig.update_traces(number=dict(font=dict(color='#FFFFFF', size=40)))
    return fig

def plot_probability_distribution(probs_dict):
    """
    Menampilkan distribusi probabilitas kelas menggunakan grafik batang horizontal interaktif.
    """
    df_probs = pd.DataFrame(list(probs_dict.items()), columns=['Status Gizi', 'Probabilitas (%)'])
    df_probs = df_probs.sort_values(by='Probabilitas (%)', ascending=True)
    
    df_probs['Status Gizi'] = df_probs['Status Gizi'].str.title()
    
    fig = px.bar(
        df_probs,
        x='Probabilitas (%)',
        y='Status Gizi',
        orientation='h',
        color='Status Gizi',
        color_discrete_map={k.title(): v for k, v in COLOR_MAP.items()},
        title='Distribusi Probabilitas Kelas',
        text='Probabilitas (%)'
    )
    
    fig = apply_dark_theme(fig, height=300)
    fig.update_layout(showlegend=False)
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside', textfont=dict(color='#FFFFFF'))
    fig.update_xaxes(range=[0, 110]) 
    return fig

def plot_probability_pie(probs_dict):
    """
    Menampilkan grafik pie komposisi probabilitas prediksi.
    """
    df_probs = pd.DataFrame(list(probs_dict.items()), columns=['Status Gizi', 'Probabilitas (%)'])
    df_probs['Status Gizi'] = df_probs['Status Gizi'].str.title()
    
    fig = px.pie(
        df_probs, 
        values='Probabilitas (%)', 
        names='Status Gizi',
        color='Status Gizi',
        color_discrete_map={k.title(): v for k, v in COLOR_MAP.items()},
        title='Komposisi Probabilitas Prediksi'
    )
    
    fig = apply_dark_theme(fig, height=300)
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    fig.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='#FFFFFF'))
    return fig
