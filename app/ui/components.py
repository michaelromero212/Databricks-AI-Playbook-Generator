import streamlit as st

def set_page_config():
    st.set_page_config(
        page_title="Databricks AI Playbook Generator",
        page_icon="DB",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS with WCAG AA accessibility standards
    st.markdown("""
        <style>
        /* Main container - accessible white background */
        .main {
            background-color: #FFFFFF;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
        }
        
        /* Typography - high contrast for readability */
        h1, h2, h3 {
            color: #1F2937;  /* 12:1 contrast on white - exceeds WCAG AAA */
            font-weight: 600;
            line-height: 1.4;
            margin-bottom: 0.75rem;
        }
        
        h1 {
            font-size: 2.25rem;
        }
        
        h2 {
            font-size: 1.875rem;
        }
        
        h3 {
            font-size: 1.5rem;
        }
        
        p, li, span {
            color: #374151;  /* 9.7:1 contrast - WCAG AAA */
            font-size: 1rem;
        }
        
        
        /* Primary buttons - FORCE white text with multiple selectors */
        .stButton>button,
        .stButton>button *,
        .stButton>button span,
        .stButton>button p,
        .stButton>button div,
        button[kind="primary"],
        button[kind="secondary"] {
            background-color: #0066CC !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            border: 2px solid transparent !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
        }
        
        /* Force white text on all button children */
        .stButton button * {
            color: #FFFFFF !important;
        }
        
        .stButton>button:hover,
        .stButton>button:hover *,
        button[kind="primary"]:hover,
        button[kind="secondary"]:hover {
            background-color: #0052A3 !important;
            color: #FFFFFF !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
        }
        
        /* Focus states for keyboard navigation */
        .stButton>button:focus,
        .stButton>button:focus-visible {
            outline: 3px solid #0066CC !important;
            outline-offset: 3px !important;
            border: 2px solid #0066CC !important;
            color: #FFFFFF !important;
        }
        
        /* Cards with accessible contrast */
        .card {
            background-color: #F9FAFB;  /* Light gray background */
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            border: 1px solid #E5E7EB;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #F9FAFB;
            border-right: 1px solid #E5E7EB;
        }
        
        [data-testid="stSidebar"] h2 {
            color: #1F2937;
        }
        
        /* File uploader - enhanced accessibility */
        [data-testid="stFileUploadDropzone"] {
            border: 2px dashed #9CA3AF;
            border-radius: 8px;
            background-color: #FFFFFF;
        }
        
        [data-testid="stFileUploadDropzone"]:hover {
            border-color: #0066CC;
            background-color: #F0F7FF;
        }
        
        /* Text input areas */
        textarea, input {
            border: 2px solid #D1D5DB !important;
            border-radius: 6px !important;
            font-size: 1rem !important;
            color: #1F2937 !important;
        }
        
        textarea:focus, input:focus {
            border-color: #0066CC !important;
            outline: none !important;
            box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1) !important;
        }
        
        /* Success messages - colorblind-safe teal */
        .stSuccess {
            background-color: #D1FAE5;
            border-left: 4px solid #067D62;
            color: #065F46;
            padding: 12px;
            border-radius: 6px;
        }
        
        /* Warning messages - colorblind-safe amber */
        .stWarning {
            background-color: #FEF3C7;
            border-left: 4px solid #D97706;
            color: #92400E;
            padding: 12px;
            border-radius: 6px;
        }
        
        /* Info messages */
        .stInfo {
            background-color: #DBEAFE;
            border-left: 4px solid #0066CC;
            color: #1E3A8A;
            padding: 12px;
            border-radius: 6px;
        }
        
        /* Error messages - high contrast red */
        .stError {
            background-color: #FEE2E2;
            border-left: 4px solid #DC2626;
            color: #991B1B;
            padding: 12px;
            border-radius: 6px;
        }
        
        /* Tabs - accessible styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #4B5563;
            font-weight: 500;
            padding: 12px 20px;
            border-bottom: 3px solid transparent;
        }
        
        .stTabs [aria-selected="true"] {
            color: #0066CC;
            border-bottom-color: #0066CC;
            font-weight: 600;
        }
        
        /* Download buttons - secondary style */
        .stDownloadButton>button {
            background-color: #FFFFFF !important;
            color: #0066CC !important;
            border: 2px solid #0066CC !important;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        
        .stDownloadButton>button:hover {
            background-color: #F0F7FF !important;
            color: #0066CC !important;
            transform: translateY(-1px);
        }
        
        /* Code blocks - high contrast */
        code {
            background-color: #F3F4F6;
            color: #1F2937;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
        }
        
        pre {
            background-color: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            padding: 16px;
        }
        
        /* Links - accessible color and underline */
        a {
            color: #0066CC;
            text-decoration: underline;
            font-weight: 500;
        }
        
        a:hover {
            color: #0052A3;
        }
        
        a:focus {
            outline: 3px solid #0066CC;
            outline-offset: 2px;
        }
        
        /* AGGRESSIVE BUTTON FIX - Override all possible Streamlit selectors */
        button[data-testid="baseButton-primary"],
        button[data-testid="baseButton-secondary"],
        button[class*="stButton"],
        div[data-testid*="stButton"] button,
        div[class*="stButton"] button {
            background-color: #0066CC !important;
            color: white !important;
        }
        
        button[data-testid="baseButton-primary"] *,
        button[data-testid="baseButton-secondary"] *,
        div[data-testid*="stButton"] button *,
        div[class*="stButton"] button * {
            color: white !important;
        }
        
        /* Override Streamlit's default button text color */
        .stButton button p,
        .stButton button span,
        .stButton button div {
            color: #FFFFFF !important;
        }
        
        /* Ensure hover states maintain white text */
        button[data-testid="baseButton-primary"]:hover,
        button[data-testid="baseButton-secondary"]:hover {
            background-color: #0052A3 !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

def header():
    st.title("Databricks AI Playbook Generator")
    st.markdown("Generate professional delivery playbooks from your project artifacts.")
    st.markdown("---")

def card(title, content):
    st.markdown(f"""
    <div class="card">
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)
