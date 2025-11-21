import streamlit as st

def set_page_config():
    st.set_page_config(
        page_title="Databricks AI Playbook Generator",
        page_icon="📘",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for Apple-style minimalism
    st.markdown("""
        <style>
        .main {
            background-color: #FFFFFF;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        h1, h2, h3 {
            color: #1D1D1F;
            font-weight: 600;
        }
        .stButton>button {
            background-color: #0071e3;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            font-weight: 500;
        }
        .stButton>button:hover {
            background-color: #0077ed;
        }
        .card {
            background-color: #F5F5F7;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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
