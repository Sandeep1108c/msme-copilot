"""
🚀 MSME Copilot - AI-Powered Business Consultant & Market Research Agent

Main Streamlit Application with Premium UI/UX
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import time
import base64

# Page config must be first Streamlit command
st.set_page_config(
    page_title="MSME Copilot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

from config import APP_TITLE, APP_SUBTITLE, BUSINESS_TYPES
from agents import AgentOrchestrator
from ui.components import (
    render_analysis_results,
    render_sources_sidebar,
    render_strategy_report,
    render_weekly_plan,
    render_verification_badge,
    render_category_analysis
)
from utils.pdf_generator import generate_strategy_pdf

# Load and encode logo
def get_logo_base64():
    logo_path = Path("assets/logo_gold.png")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# Load and encode feature icons
def get_icon_base64(icon_name):
    icon_path = Path(f"assets/{icon_name}")
    if icon_path.exists():
        with open(icon_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


# Premium CSS with animations and modern design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #111111 40%, #0d0d0d 70%, #0a0a0a 100%);
    }
    
    /* Hide Streamlit branding but keep sidebar toggle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Style Streamlit's native sidebar toggle button - Gold theme */
    [data-testid="stSidebarCollapsedControl"] {
        position: fixed !important;
        top: 15px !important;
        left: 15px !important;
        z-index: 999999 !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] button {
        background: linear-gradient(135deg, #c9a227 0%, #d4a574 50%, #c9a227 100%) !important;
        border: 1px solid rgba(212, 165, 116, 0.5) !important;
        border-radius: 12px !important;
        width: 50px !important;
        height: 50px !important;
        box-shadow: 0 4px 20px rgba(201, 162, 39, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] button:hover {
        transform: translateY(-2px) scale(1.05) !important;
        box-shadow: 0 6px 30px rgba(201, 162, 39, 0.6) !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] button svg {
        width: 24px !important;
        height: 24px !important;
        stroke: #0a0a0a !important;
    }
    
    /* Main header with dark glass and gold accents */
    .main-header {
        background: linear-gradient(135deg, rgba(20, 20, 20, 0.95) 0%, rgba(30, 25, 15, 0.95) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 2.5rem 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(212, 165, 116, 0.2);
        border: 1px solid rgba(201, 162, 39, 0.3);
        animation: fadeInDown 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #c9a227, #f5d061, #c9a227, transparent);
        animation: goldShimmer 3s ease-in-out infinite;
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #f5d061 0%, #c9a227 50%, #d4a574 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        font-size: 1.15rem;
        opacity: 0.85;
        font-weight: 300;
        color: #b0a090;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes goldGlow {
        0%, 100% { box-shadow: 0 0 5px rgba(201, 162, 39, 0.3), 0 0 10px rgba(201, 162, 39, 0.1); }
        50% { box-shadow: 0 0 20px rgba(201, 162, 39, 0.5), 0 0 40px rgba(212, 165, 116, 0.3); }
    }
    
    @keyframes goldShimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    @keyframes borderGlow {
        0%, 100% { border-color: rgba(201, 162, 39, 0.3); }
        50% { border-color: rgba(201, 162, 39, 0.6); }
    }
    
    /* Agent pipeline cards - Dark with gold accents */
    .agent-card {
        background: linear-gradient(145deg, rgba(25, 25, 25, 0.9) 0%, rgba(15, 15, 15, 0.9) 100%);
        backdrop-filter: blur(10px);
        padding: 1.2rem;
        border-radius: 16px;
        text-align: center;
        min-height: 130px;
        border: 1px solid rgba(201, 162, 39, 0.15);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: fadeInUp 0.6s ease-out;
    }
    
    .agent-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 40px rgba(201, 162, 39, 0.2);
        border-color: rgba(201, 162, 39, 0.5);
    }
    
    .agent-card.active {
        animation: goldGlow 2s ease-in-out infinite;
        border-color: rgba(201, 162, 39, 0.8);
    }
    
    .agent-card.complete {
        background: linear-gradient(145deg, rgba(34, 45, 30, 0.9) 0%, rgba(20, 30, 15, 0.9) 100%);
        border-color: rgba(100, 180, 80, 0.5);
    }
    
    .agent-emoji {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .agent-name {
        font-weight: 600;
        color: #f5d061;
        font-size: 0.95rem;
        margin-bottom: 0.3rem;
    }
    
    .agent-desc {
        font-size: 0.75rem;
        color: #888;
        line-height: 1.3;
    }
    
    .agent-status {
        margin-top: 0.5rem;
        font-size: 1.2rem;
    }
    
    /* Metric cards - Dark glass with gold */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(25, 25, 25, 0.9) 0%, rgba(18, 18, 18, 0.9) 100%);
        backdrop-filter: blur(10px);
        padding: 1.2rem 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(201, 162, 39, 0.15);
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(201, 162, 39, 0.15);
        border-color: rgba(201, 162, 39, 0.4);
    }
    
    [data-testid="stMetricLabel"] {
        color: #b0a090 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #f5d061 !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    
    /* Tab styling - Gold highlights */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(20, 20, 20, 0.8);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(201, 162, 39, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #a0a0a0;
        font-weight: 500;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(201, 162, 39, 0.15);
        color: #f5d061;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #c9a227 0%, #d4a574 100%) !important;
        color: #0a0a0a !important;
        font-weight: 600 !important;
    }
    
    /* Progress bar - Gold shimmer */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #c9a227 0%, #f5d061 25%, #d4a574 50%, #f5d061 75%, #c9a227 100%);
        border-radius: 10px;
        animation: shimmer 2s infinite;
        background-size: 2000px 100%;
    }
    
    .stProgress > div > div > div {
        background: rgba(201, 162, 39, 0.1);
        border-radius: 10px;
    }
    
    /* Button styling - Gold gradient */
    .stButton > button {
        background: linear-gradient(135deg, #c9a227 0%, #d4a574 50%, #c9a227 100%);
        color: #0a0a0a;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 20px rgba(201, 162, 39, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 35px rgba(201, 162, 39, 0.5);
        background: linear-gradient(135deg, #d4a574 0%, #f5d061 50%, #d4a574 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Success banner - Muted gold-green */
    .success-banner {
        background: linear-gradient(135deg, rgba(50, 60, 40, 0.95) 0%, rgba(35, 45, 25, 0.95) 100%);
        backdrop-filter: blur(10px);
        color: #c0d0a0;
        padding: 1.2rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin: 1.5rem 0;
        font-weight: 500;
        font-size: 1.1rem;
        animation: fadeInUp 0.6s ease-out, pulse 2s ease-in-out 0.6s;
        box-shadow: 0 8px 32px rgba(100, 120, 80, 0.2);
        border: 1px solid rgba(100, 140, 60, 0.3);
    }
    
    /* Sidebar styling - Deep black with gold */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d0d 0%, #111111 50%, #0a0a0a 100%);
        border-right: 1px solid rgba(201, 162, 39, 0.15);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #d0d0d0;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #f5d061 !important;
    }
    
    /* Expander styling - Dark with gold border */
    .streamlit-expanderHeader {
        background: rgba(20, 20, 20, 0.9);
        border-radius: 10px;
        border: 1px solid rgba(201, 162, 39, 0.15);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(30, 28, 20, 0.9);
        border-color: rgba(201, 162, 39, 0.4);
    }
    
    /* DataFrame styling */
    [data-testid="stDataFrame"] {
        background: rgba(15, 15, 15, 0.9);
        border-radius: 12px;
        border: 1px solid rgba(201, 162, 39, 0.15);
        animation: fadeIn 0.5s ease-out;
    }
    
    /* File uploader - Gold dashed border */
    [data-testid="stFileUploader"] {
        background: rgba(15, 15, 15, 0.8);
        border-radius: 12px;
        border: 2px dashed rgba(201, 162, 39, 0.4);
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(201, 162, 39, 0.8);
        background: rgba(25, 22, 15, 0.8);
    }
    
    /* Checkbox styling */
    .stCheckbox {
        transition: all 0.2s ease;
    }
    
    .stCheckbox:hover {
        background: rgba(201, 162, 39, 0.05);
        border-radius: 8px;
    }
    
    /* Info/Warning boxes */
    .stInfo, .stWarning, .stSuccess, .stError {
        border-radius: 12px;
        border: none;
        animation: fadeInUp 0.5s ease-out;
    }
    
    /* Welcome section - Dark premium glass */
    .welcome-section {
        background: linear-gradient(145deg, rgba(20, 20, 20, 0.95) 0%, rgba(15, 15, 15, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2.5rem;
        border: 1px solid rgba(201, 162, 39, 0.2);
        animation: fadeInUp 0.8s ease-out;
        position: relative;
    }
    
    .welcome-section::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(201, 162, 39, 0.5), transparent);
    }
    
    .welcome-section h2 {
        color: #f5d061;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    .welcome-section p, .welcome-section li {
        color: #b0b0b0;
        line-height: 1.7;
    }
    
    /* Feature cards - Dark with gold accents */
    .feature-card {
        background: linear-gradient(145deg, rgba(25, 23, 18, 0.9) 0%, rgba(18, 16, 12, 0.9) 100%);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(201, 162, 39, 0.2);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(201, 162, 39, 0.5);
        box-shadow: 0 8px 30px rgba(201, 162, 39, 0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        color: #f5d061;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #909090;
        font-size: 0.9rem;
    }
    
    /* Status text */
    .status-text {
        color: #b0a090;
        font-size: 0.9rem;
        text-align: center;
        padding: 1rem;
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Scrollbar styling - Gold */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(20, 20, 20, 0.8);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #c9a227 0%, #d4a574 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #d4a574 0%, #f5d061 100%);
    }
    
    /* Strategy report styling */
    .strategy-report {
        background: linear-gradient(145deg, rgba(20, 20, 20, 0.95) 0%, rgba(15, 15, 15, 0.95) 100%);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(201, 162, 39, 0.15);
        animation: fadeIn 0.6s ease-out;
    }
    
    .strategy-report h1, .strategy-report h2, .strategy-report h3 {
        color: #f5d061;
    }
    
    .strategy-report p, .strategy-report li {
        color: #c0c0c0;
    }
    
    /* Table styling - Gold headers */
    .strategy-report table {
        background: rgba(15, 15, 15, 0.9);
        border-radius: 8px;
        overflow: hidden;
    }
    
    .strategy-report th {
        background: linear-gradient(135deg, rgba(201, 162, 39, 0.3) 0%, rgba(180, 140, 30, 0.3) 100%);
        color: #f5d061;
    }
    
    .strategy-report td {
        border-color: rgba(201, 162, 39, 0.1);
        color: #c0c0c0;
    }
    
    /* Custom tooltip styling - Black-Gold */
    .custom-tooltip {
        position: relative;
        display: inline-block;
        width: 100%;
    }
    
    .custom-tooltip .tooltip-text {
        visibility: hidden;
        opacity: 0;
        background: linear-gradient(135deg, rgba(20, 18, 12, 0.98) 0%, rgba(30, 25, 15, 0.98) 100%);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        color: #f5d061;
        text-align: center;
        border-radius: 12px;
        padding: 12px 16px;
        position: absolute;
        z-index: 999999;
        bottom: 110%;
        left: 50%;
        transform: translateX(-50%);
        min-width: 220px;
        font-size: 0.85rem;
        font-weight: 400;
        line-height: 1.4;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), 0 0 20px rgba(201, 162, 39, 0.15);
        border: 1px solid rgba(201, 162, 39, 0.4);
        transition: all 0.3s ease;
    }
    
    .custom-tooltip .tooltip-text::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -8px;
        border-width: 8px;
        border-style: solid;
        border-color: rgba(30, 25, 15, 0.98) transparent transparent transparent;
    }
    
    .custom-tooltip:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    
    /* Select boxes and inputs */
    .stSelectbox > div > div {
        background: rgba(20, 20, 20, 0.9) !important;
        border: 1px solid rgba(201, 162, 39, 0.2) !important;
        border-radius: 10px !important;
    }
    
    .stTextInput > div > div > input {
        background: rgba(20, 20, 20, 0.9) !important;
        border: 1px solid rgba(201, 162, 39, 0.2) !important;
        color: #e0e0e0 !important;
        border-radius: 10px !important;
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(20, 20, 20, 0.9) !important;
        border: 1px solid rgba(201, 162, 39, 0.2) !important;
        color: #e0e0e0 !important;
        border-radius: 10px !important;
    }
    
    /* Links */
    a {
        color: #f5d061 !important;
        transition: all 0.2s ease;
    }
    
    a:hover {
        color: #d4a574 !important;
    }
    
    /* Gold glow effect for all emojis */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    .stMarkdown p, .stMarkdown li, .stMarkdown span, .stMarkdown div,
    .stTabs [data-baseweb="tab"] {
        text-shadow: none;
    }
    
    /* Apply gold filter to emoji characters */
    .stMarkdown h1::first-letter, .stMarkdown h2::first-letter, .stMarkdown h3::first-letter {
        filter: drop-shadow(0 0 8px rgba(245, 208, 97, 0.6));
    }
    
    /* Gold glow for tab labels with emojis */
    .stTabs [data-baseweb="tab"] {
        text-shadow: 0 0 10px rgba(201, 162, 39, 0.3);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        text-shadow: 0 0 15px rgba(245, 208, 97, 0.5);
    }
    
    /* Enhanced emoji styling - gold glow on headers */
    h1, h2, h3, h4, h5, h6 {
        text-shadow: 0 0 20px rgba(201, 162, 39, 0.15);
    }
    
    /* Gold accent for bullet points and list items */
    .stMarkdown ul li::marker, .stMarkdown ol li::marker {
        color: #c9a227;
    }
    
    /* Strategy report emoji enhancement */
    .stMarkdown strong {
        color: #f5d061;
    }
</style>
""", unsafe_allow_html=True)


def render_header():
    """Render the main app header with custom logo"""
    logo_base64 = get_logo_base64()
    
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="height: 70px; margin-right: 15px; vertical-align: middle; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));">'
    else:
        logo_html = ''
    
    st.markdown(f"""
    <div class="main-header">
        <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
            {logo_html}
            <div>
                <h1 style="margin: 0; font-size: 2.5rem; background: linear-gradient(135deg, #f5d061 0%, #c9a227 50%, #d4a574 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                    MSME Copilot
                </h1>
            </div>
        </div>
        <p style="margin-top: 0.8rem; font-size: 1.1rem; opacity: 0.9; letter-spacing: 0.5px;">
            AI-Powered Business Consultant &amp; Market Research Agent
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_agent_pipeline(current_agent: str, progress: float, status: str):
    """Render the 5-agent pipeline progress with animations"""
    
    agents = [
        ("📊", "Data Analyst", "Analyzing sales"),
        ("📋", "Planner", "Creating tasks"),
        ("🔍", "Researcher", "Web research"),
        ("🔎", "Critic", "Verifying data"),
        ("📝", "Consultant", "Strategy")
    ]
    
    cols = st.columns(5)
    
    for i, (emoji, name, desc) in enumerate(agents):
        agent_progress = (i + 1) / 5
        
        with cols[i]:
            if progress >= agent_progress:
                status_icon = "✅"
                card_class = "agent-card complete"
            elif progress >= (i / 5) and progress < agent_progress:
                status_icon = "🔄"
                card_class = "agent-card active"
            else:
                status_icon = "⏳"
                card_class = "agent-card"
            
            st.markdown(f"""
            <div class="{card_class}" style="animation-delay: {i * 0.1}s">
                <span class="agent-emoji">{emoji}</span>
                <div class="agent-name">{name}</div>
                <div class="agent-desc">{desc}</div>
                <div class="agent-status">{status_icon}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(progress)
    st.markdown(f'<p class="status-text">{status}</p>', unsafe_allow_html=True)


def render_welcome():
    """Render beautiful welcome section"""
    st.markdown("""
    <div class="welcome-section" style="background: linear-gradient(145deg, rgba(201, 162, 39, 0.08) 0%, rgba(15, 15, 15, 0.95) 100%); border: 1px solid rgba(201, 162, 39, 0.25);">
        <h2 style="color: #f5d061; margin-bottom: 0.5rem;">✨ Welcome to MSME Copilot!</h2>
        <p style="font-size: 1.1rem; margin-bottom: 2rem; color: #b0a090;">
            Your AI-powered business consultant that analyzes data, researches markets, and creates actionable strategies.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature cards with gold icons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon"><img src="data:image/png;base64,""" + (get_icon_base64("icon_smart_analysis.png") or "") + """" style="height: 48px; width: 48px; object-fit: contain;"></div>
            <div class="feature-title">Smart Analysis</div>
            <div class="feature-desc">Analyzes your sales data for profit trends and weak products</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon"><img src="data:image/png;base64,""" + (get_icon_base64("icon_market_research.png") or "") + """" style="height: 48px; width: 48px; object-fit: contain;"></div>
            <div class="feature-title">Market Research</div>
            <div class="feature-desc">Autonomously researches competitors and market trends</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon"><img src="data:image/png;base64,""" + (get_icon_base64("icon_verified_sources.png") or "") + """" style="height: 48px; width: 48px; object-fit: contain;"></div>
            <div class="feature-title">Verified Sources</div>
            <div class="feature-desc">All recommendations backed by real sources you can check</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon"><img src="data:image/png;base64,""" + (get_icon_base64("icon_action_plan.png") or "") + """" style="height: 48px; width: 48px; object-fit: contain;"></div>
            <div class="feature-title">Action Plan</div>
            <div class="feature-desc">Get a concrete 4-week plan you can start implementing today</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Getting started
    st.markdown("""
    <div class="welcome-section" style="background: linear-gradient(145deg, rgba(201, 162, 39, 0.08) 0%, rgba(180, 140, 30, 0.08) 100%); border: 1px solid rgba(201, 162, 39, 0.2);">
        <h3 style="color: #f5d061;">⚡ Getting Started</h3>
        <ol style="margin-left: 1.5rem; color: #b0a090;">
            <li>Upload your sales CSV file</li>
            <li>Select your business type</li>
            <li>Optionally set a specific business goal</li>
            <li>Click <strong style="color: #f5d061;">Run MSME Copilot</strong> and watch the magic!</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # CSV Format info
    with st.expander("📄 Expected CSV Format"):
        st.markdown("""
        Your CSV should have these columns:
        
        | Column | Description | Example |
        |--------|-------------|---------|
        | product_name | Name of the product | Rice (5kg) |
        | category | Product category (optional) | Groceries |
        | quantity_sold | Units sold | 45 |
        | unit_price | Selling price per unit | 280 |
        | unit_cost | Cost per unit | 220 |
        | date | Date of sale | 2024-01-15 |
        | stock_remaining | Current inventory (optional) | 120 |
        """)


def main():
    """Main application entry point"""
    
    render_header()
    
    # Initialize session state
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = None
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'running' not in st.session_state:
        st.session_state.running = False
    
    # Sidebar - Input Section
    with st.sidebar:
        # Upload Data header with gold icon
        upload_icon = get_icon_base64("icon_upload_data.png")
        if upload_icon:
            st.markdown(f'<h3 style="color: #f5d061; display: flex; align-items: center; gap: 10px;"><img src="data:image/png;base64,{upload_icon}" style="height: 28px; width: 28px;"> Upload Data</h3>', unsafe_allow_html=True)
        else:
            st.markdown("### 📤 Upload Data")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Sales CSV File",
            type=['csv'],
            help="Upload your sales data in CSV format",
            key="sidebar_uploader"
        )
        
        st.markdown("---")
        
        # Business configuration
        # Configuration header with gold icon
        config_icon = get_icon_base64("icon_configuration.png")
        if config_icon:
            st.markdown(f'<h3 style="color: #f5d061; display: flex; align-items: center; gap: 10px;"><img src="data:image/png;base64,{config_icon}" style="height: 28px; width: 28px;"> Configuration</h3>', unsafe_allow_html=True)
        else:
            st.markdown("### ⚙️ Configuration")
        
        business_type = st.selectbox(
            "Business Type",
            BUSINESS_TYPES,
            index=0,
            key="sidebar_business"
        )
        
        ceo_goal = st.text_area(
            "CEO's Goal (Optional)",
            placeholder="e.g., Increase profit by 15%",
            height=80,
            key="sidebar_goal"
        )
        
        st.markdown("---")
        
        # Run button
        can_run = uploaded_file is not None
        
        run_analysis = st.button(
            "⚡ Run MSME Copilot",
            type="primary",
            disabled=not can_run,
            use_container_width=True,
            key="sidebar_run"
        )
        
        if not can_run:
            st.warning("Please upload a CSV file to continue")
        
        # Sources section (populated after analysis)
        if st.session_state.results:
            sources = st.session_state.results.get('sources', [])
            if sources:
                render_sources_sidebar(sources)
    
    
    # Main content area
    if run_analysis and can_run:
        st.session_state.running = True
        st.session_state.results = None
        
        # Determine data source
        data_source = uploaded_file
        
        # Create orchestrator and run
        orchestrator = AgentOrchestrator()
        st.session_state.orchestrator = orchestrator
        
        # Progress containers
        # AI Agents Working header with gold icon
        ai_icon = get_icon_base64("icon_ai_agents.png")
        if ai_icon:
            st.markdown(f'<h3 style="color: #f5d061; display: flex; align-items: center; gap: 10px;"><img src="data:image/png;base64,{ai_icon}" style="height: 32px; width: 32px;"> AI Agents Working...</h3>', unsafe_allow_html=True)
        else:
            st.markdown("### 🤖 AI Agents Working...")
        pipeline_placeholder = st.empty()
        
        # Progress callback
        def update_ui(agent: str, progress: float, status: str):
            with pipeline_placeholder:
                render_agent_pipeline(agent, progress, status)
            time.sleep(0.1)
        
        # Run the pipeline
        with st.spinner(""):
            results = orchestrator.run_pipeline(
                sales_file=data_source,
                business_type=business_type,
                ceo_goal=ceo_goal if ceo_goal else None,
                progress_callback=update_ui
            )
        
        st.session_state.results = results.get('results', {})
        st.session_state.running = False
        
        if results.get('success'):
            st.markdown("""
            <div class="success-banner">
                🎉 Analysis Complete! Your personalized business strategy is ready below.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"Analysis failed: {results.get('error', 'Unknown error')}")
    
    # Display results if available
    if st.session_state.results and not st.session_state.running:
        results = st.session_state.results
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tab navigation for results
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Analysis",
            "🔍 Verification", 
            "📜 Strategy",
            "📅 Weekly Plan"
        ])
        
        with tab1:
            analysis = results.get('analysis', {})
            if analysis:
                render_analysis_results(analysis)
                render_category_analysis(analysis)
        
        with tab2:
            verification = results.get('verification', {})
            if verification:
                render_verification_badge(verification)
                
                st.markdown("---")
                
                # Show verified recommendations
                verified = verification.get('verification', {}).get('verified_recommendations', [])
                if verified:
                    st.subheader("✅ Verified Recommendations")
                    for rec in verified:
                        confidence = rec.get('confidence', 'medium')
                        emoji = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(confidence, "⚪")
                        
                        with st.expander(f"{emoji} {rec.get('recommendation', 'Recommendation')[:60]}..."):
                            st.markdown(f"**Evidence:** {rec.get('evidence', 'N/A')}")
                            st.markdown(f"**Potential Impact:** {rec.get('potential_impact', 'Unknown')}")
                            st.markdown(f"**Sources:** {rec.get('sources_count', 0)} sources")
                
                # Show conflicts
                conflicts = verification.get('verification', {}).get('conflicts_found', [])
                if conflicts:
                    st.subheader("⚠️ Conflicts Detected")
                    for conflict in conflicts:
                        st.warning(f"**Issue:** {conflict.get('issue')}\n\n**Resolution:** {conflict.get('resolution')}")
        
        with tab3:
            final_report = results.get('final_report', '')
            if final_report:
                st.markdown('<div class="strategy-report">', unsafe_allow_html=True)
                render_strategy_report(final_report)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Strategy report is being generated...")
        
        with tab4:
            strategy = results.get('strategy', {})
            if strategy:
                render_weekly_plan(strategy)
                
                st.markdown("---")
                st.markdown("### 📥 Download Your Strategy")
                col1, col2 = st.columns([1, 1])
                
                # Get the actual strategy data for PDF
                strategy_data = strategy.get('strategy', strategy)
                
                with col1:
                    st.download_button(
                        "📄 Download as Markdown",
                        results.get('final_report', ''),
                        file_name="msme_copilot_strategy.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                with col2:
                    # Generate PDF
                    try:
                        pdf_bytes = generate_strategy_pdf(strategy_data)
                        st.download_button(
                            "📑 Download as PDF",
                            pdf_bytes,
                            file_name="msme_copilot_strategy.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"PDF generation failed: {str(e)}")
    
    # Show welcome message if no results
    if not st.session_state.results and not st.session_state.running:
        render_welcome()


if __name__ == "__main__":
    main()
