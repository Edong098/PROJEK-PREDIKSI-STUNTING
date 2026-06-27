import streamlit as st
import os
import base64

# Set page config as the very first command
st.set_page_config(
    page_title="Prediksi Stunting & Status Gizi",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_custom_css():
    """
    Injects custom Google Fonts and a premium Dark-Mode theme (Slate Black, Neon Green, Light Blue)
    with semi-transparent white-accented glassmorphism cards. Enforces pure white text colors.
    """
    st.markdown("""
    <style>
    /* Import modern typography from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Apply fonts globally and enforce pure white text colors for readability */
    html, body, [class*="css"], .stMarkdown, p, span, li, label, div, small {
        font-family: 'Plus Jakarta Sans', 'Outfit', sans-serif;
        color: #FFFFFF !important; /* Pure white text */
    }
    
    /* Dark theme background */
    .stApp {
        background: radial-gradient(circle at 20% 30%, #0F1D19 0%, #0B1116 100%);
    }
    
    /* Header titles in bright white */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        color: #FFFFFF !important; 
        min-height: auto;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Premium Glassmorphism Card (Dark background with white borders) */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.12) !important; /* Brighter white blend border */
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        margin-bottom: 12px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: justify !important;
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
        word-break: break-word;
    }
    .glass-card h4, .glass-card p {
        margin: 0.5rem 0;
    }
    
    .glass-card p, .glass-card h4, .glass-card h5, .glass-card span, .glass-card div {
        text-align: justify !important;
    }
    .glass-card h4 { text-align: left !important; width: 100%; white-space: normal; overflow: visible; }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border: 1px solid rgba(46, 204, 113, 0.4) !important; /* Stronger green glow on hover */
        box-shadow: 0 12px 35px rgba(46, 204, 113, 0.08);
    }
    
    /* Form styles overrides */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 20px !important;
    }
    
    /* Inputs text coloring */
    input, select, textarea, div[role="listbox"] {
        color: #FFFFFF !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Metrics container override for dark mode */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2ECC71 !important; /* Keep Neon green value */
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        font-weight: 600;
        color: #FFFFFF !important; /* Pure white label */
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Dark-mode Sidebar customization */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #08110D !important; /* Extremely dark forest green */
        border-right: 1px solid rgba(46, 204, 113, 0.2);
    }
    
    /* Sidebar texts and headers */
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] li {
        color: #FFFFFF !important;
    }
    
    /* Premium custom buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #2ECC71 0%, #15803D 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3) !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(46, 204, 113, 0.45) !important;
        border: none !important;
    }
    
    /* Tabs styling for Dark Mode */
    button[data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-weight: 600 !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2ECC71 !important;
        border-bottom-color: #2ECC71 !important;
    }
    
    /* Table modifications */
    table {
        background-color: rgba(255, 255, 255, 0.02) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    th {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-bottom: 2px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    td {
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    /* Responsive styles for mobile (Bisa dibuka di HP) */
    @media (max-width: 768px) {
        /* Stack Streamlit columns vertically on small screens */
        .stColumns > div {
            width: 100% !important;
            margin-bottom: 1rem !important;
        }
        /* Reduce glass-card padding for tighter space on mobile */
        .glass-card {
            padding: 16px;
        }
        
        .stApp {
            padding: 10px !important;
        }
        
        h1 {
            font-size: 1.8rem !important;
        }
        
        h2 {
            font-size: 1.4rem !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.6rem !important;
        }
        
        div.stButton > button {
            width: 100% !important; /* Full width button on mobile */
            padding: 12px 10px !important;
        }
    }
    
    /* Compact horizontal lines (mencegah jarak terlalu jauh) */
    hr {
        margin-top: 12px !important;
        margin-bottom: 12px !important;
        border: none !important;
        border-top: 1px solid rgba(255, 255, 255, 0.18) !important;
    }
    
    /* Decorative Neon Gradient Header */
    .gradient-text {
        background: linear-gradient(135deg, #2ECC71 0%, #3498DB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    </style>
    """, unsafe_allow_html=True)

# Run CSS injection globally
inject_custom_css()

# Configure Multi-page Navigation
try:
    home_page = st.Page("pages/1_Home.py", title="Home", icon="🏠", default=True)
    dataset_page = st.Page("pages/2_Dataset.py", title="Dataset", icon="📊")
    eda_page = st.Page("pages/3_EDA.py", title="Exploratory Data Analysis", icon="📈")
    model_page = st.Page("pages/4_Model.py", title="Model Evaluation", icon="🤖")
    prediksi_page = st.Page("pages/5_Prediksi.py", title="Prediksi Status Gizi", icon="🔮")
    tentang_page = st.Page("pages/6_Tentang.py", title="Tentang Peneliti", icon="ℹ️")
    


    pg = st.navigation(
        [home_page, dataset_page, eda_page, model_page, prediksi_page, tentang_page],
        position="hidden" # Hide the default Streamlit page navigation list
    )
    
    # Custom Sidebar Layout (Ensures correct order: Header -> Links -> Footer)
    with st.sidebar:
        # 1. Sidebar Header (Always at the top)
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as image_file:
                encoded_logo = base64.b64encode(image_file.read()).decode()
            logo_html = f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-top: 5px; margin-bottom: 5px;">
                <img src="data:image/png;base64,{encoded_logo}" style="width: 35px; height: 35px; border-radius: 50%; object-fit: cover; border: 1px solid rgba(255,255,255,0.2);">
                <h3 style="color: #FFFFFF; font-weight: 700; margin: 0; font-family: 'Outfit', sans-serif; font-size: 1.3rem; line-height: 1.2;">PREDIKSI STUNTING</h3>
            </div>
            """
            st.markdown(logo_html, unsafe_allow_html=True)
        else:
            st.markdown('<h3 style="color: #FFFFFF; font-weight: 700; margin-top: 10px; margin-bottom: 5px;">PREDIKSI STUNTING</h3>', unsafe_allow_html=True)
        st.write("---")
        
        # 2. Navigation Links (In the middle)
        st.page_link("pages/1_Home.py", label="Home", icon="🏠")
        st.page_link("pages/2_Dataset.py", label="Dataset", icon="📊")
        st.page_link("pages/3_EDA.py", label="Exploratory Data Analysis", icon="📈")
        st.page_link("pages/4_Model.py", label="Model Evaluation", icon="🤖")
        st.page_link("pages/5_Prediksi.py", label="Prediksi Status Gizi", icon="🔮")
        st.page_link("pages/6_Tentang.py", label="Tentang Peneliti", icon="ℹ️")
        
        # 3. Sidebar Footer (Always at the bottom)
        st.write("---")
        st.markdown('<p style="text-align: center; color: #FFFFFF; font-weight: 600; font-size: 0.75rem; margin-top: 5px; margin-bottom: 5px;">UJIAN AKHIR SEMESTER - DATA MINING LANJUT</p>', unsafe_allow_html=True)
    
    pg.run()

except AttributeError:
    # Fallback to standard Streamlit Multi-page behavior for older versions
    import importlib.util
    
    with st.sidebar:
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as image_file:
                encoded_logo = base64.b64encode(image_file.read()).decode()
            logo_html = f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-top: 5px; margin-bottom: 5px;">
                <img src="data:image/png;base64,{encoded_logo}" style="width: 35px; height: 35px; border-radius: 50%; object-fit: cover; border: 1px solid rgba(255,255,255,0.2);">
                <h3 style="color: #FFFFFF; font-weight: 700; margin: 0; font-family: 'Outfit', sans-serif; font-size: 1.3rem; line-height: 1.2;">PREDIKSI STUNTING</h3>
            </div>
            """
            st.markdown(logo_html, unsafe_allow_html=True)
        else:
            st.markdown('<h3 style="color: #FFFFFF; font-weight: 700; margin-top: 10px; margin-bottom: 5px;">PREDIKSI STUNTING</h3>', unsafe_allow_html=True)
        st.write("---")
        
        st.page_link("pages/1_Home.py", label="Home", icon="🏠")
        st.page_link("pages/2_Dataset.py", label="Dataset", icon="📊")
        st.page_link("pages/3_EDA.py", label="Exploratory Data Analysis", icon="📈")
        st.page_link("pages/4_Model.py", label="Model Evaluation", icon="🤖")
        st.page_link("pages/5_Prediksi.py", label="Prediksi Status Gizi", icon="🔮")
        st.page_link("pages/6_Tentang.py", label="Tentang Peneliti", icon="ℹ️")
        
        st.write("---")
        st.markdown('<p style="text-align: center; color: #FFFFFF; font-weight: 600; font-size: 0.75rem; margin-top: 5px; margin-bottom: 5px;">UJIAN AKHIR SEMESTER - DATA MINING LANJUT</p>', unsafe_allow_html=True)
        
    spec = importlib.util.spec_from_file_location("home_module", "pages/1_Home.py")
    home_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(home_module)
