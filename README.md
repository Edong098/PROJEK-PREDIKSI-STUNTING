# 🍼 Prediksi Status Gizi & Risiko Stunting Balita

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-Academic-green)

> Aplikasi web berbasis Machine Learning untuk memprediksi status gizi dan risiko stunting pada balita, dikembangkan sebagai tugas **Ujian Akhir Semester (UAS) Data Mining Lanjut**.

---

## 📌 Deskripsi

Sistem ini memanfaatkan pendekatan machine learning untuk membantu mengidentifikasi status gizi anak balita (Normal, Stunting, Severely Stunting, dll.) berdasarkan fitur-fitur klinis sederhana. Bertujuan untuk mendukung deteksi dini stunting sebagai permasalahan sosial riil di Indonesia.

---

## 🚀 Fitur Utama

| Halaman | Deskripsi |
|--------|-----------|
| 🏠 **Home** | Ringkasan dataset, statistik utama, dan distribusi data |
| 📊 **Dataset** | Tampilan interaktif dataset balita |
| 🔍 **EDA** | Visualisasi eksplorasi data (countplot, histogram, boxplot, heatmap) |
| 🤖 **Model** | Perbandingan performa model, confusion matrix, feature importance |
| 🎯 **Prediksi** | Prediksi status gizi secara real-time berbasis input pengguna |
| 👥 **Tentang** | Profil tim peneliti dan kontribusi masing-masing anggota |

---

## 🧠 Model Machine Learning

Model terbaik dipilih berdasarkan **F1-Macro Score** dari tiga algoritma yang diuji:

- Logistic Regression
- Decision Tree Classifier
- **Random Forest Classifier** ✅ *(Model Terpilih)*

Teknik yang digunakan:
- **SMOTE** — menangani ketidakseimbangan kelas
- **GridSearchCV** — hyperparameter tuning
- **Standard Scaling** — normalisasi fitur numerik

---

## 📂 Struktur Proyek

```
UAS STUNTING/
│
├── app.py                          # Entry point aplikasi Streamlit
├── requirements.txt                # Daftar dependensi Python
│
├── pages/
│   ├── 1_Home.py                   # Halaman beranda & statistik
│   ├── 2_Dataset.py                # Tampilan dataset
│   ├── 3_EDA.py                    # Exploratory Data Analysis
│   ├── 4_Model.py                  # Evaluasi & perbandingan model
│   ├── 5_Prediksi.py               # Form prediksi real-time
│   └── 6_Tentang.py                # Profil tim peneliti
│
├── preprocessing/
│   ├── preprocessing.py            # Pipeline preprocessing data
│   ├── helper.py                   # Fungsi bantuan preprocessing
│   └── validation.py               # Validasi input data
│
├── model/
│   └── model_stunting.pkl          # Model Random Forest terlatih
│
├── utils/
│   ├── loader.py                   # Load dataset & model
│   ├── metrics.py                  # Perhitungan metrik evaluasi
│   ├── metrics_data.json           # Data metrik hasil training
│   ├── visualization.py            # Fungsi visualisasi Plotly
│   └── report.py                   # Fungsi laporan
│
├── assets/
│   └── logo.png                    # Aset gambar
│
└── data/
    └── data_balita.csv             # Dataset balita
```

---

## ⚙️ Instalasi & Menjalankan Lokal

### 1. Clone Repository
```bash
git clone https://github.com/Edong098/PROJEK-PREDIKSI-STUNTING.git
cd PROJEK-PREDIKSI-STUNTING
```

### 2. Buat Virtual Environment (opsional tapi disarankan)
```bash
python -m venv venv
venv\Scripts\activate       # Windows
# atau
source venv/bin/activate    # Mac/Linux
```

### 3. Install Dependensi
```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi
```bash
streamlit run app.py
```

Buka browser di `http://localhost:8501`

---

## 📊 Dataset

- **Sumber**: Data balita dari layanan kesehatan
- **Jumlah Data**: 39.425 record balita
- **Fitur Utama**: 3 fitur klinis + 1 target status gizi
- **Target Kelas**: Normal, Stunting, Severely Stunting, Wasted, Obese, dll.

---

## 👥 Tim Peneliti

| No | Nama | NIM | Kontribusi |
|----|------|-----|------------|
| 1 | Nizellya Salfani | 2301010014 | Data Understanding & Data Audit |
| 2 | Anggi Rahmawati | 2301010001 | Data Cleaning & Preprocessing |
| 3 | Daffa Dhiya Ulhaq | 2301010024 | Exploratory Data Analysis (EDA) |
| 4 | Fahmi Syarief H. | 2301010003 | Model Training Awal |
| 5 | Made Arya Sutha | 2301010030 | Hyperparameter Tuning, Ensemble & Evaluation |
| 6 | Ahmad Jul Hadi | 2301010019 | Deployment Streamlit |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit + CSS Glassmorphism
- **Backend**: Python 3.9+
- **ML Library**: Scikit-learn, Imbalanced-learn (SMOTE)
- **Visualisasi**: Plotly, Matplotlib, Seaborn
- **Data Processing**: Pandas, NumPy

---

## 📝 Mata Kuliah

> **Data Mining Lanjut** — Ujian Akhir Semester (UAS)  
> Program Studi Informatika / Ilmu Komputer

---

*Dibuat dengan ❤️ oleh Tim Kelompok UAS Data Mining Lanjut*
