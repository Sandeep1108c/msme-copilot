"""
Configuration management for MSME Copilot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model Configuration
GEMINI_MODEL = "gemini-1.5-flash"

# App Settings
APP_TITLE = "🚀 MSME Copilot"
APP_SUBTITLE = "AI-Powered Business Consultant & Market Research Agent"

# Business Types
BUSINESS_TYPES = [
    "Grocery Store",
    "Stationery Shop", 
    "Electronics Retail",
    "Clothing & Apparel",
    "Restaurant/Cafe",
    "Pharmacy",
    "Hardware Store",
    "General Store",
    "Other"
]

# Agent Configuration
MAX_SEARCH_RESULTS = 5
MAX_SOURCES_PER_TASK = 3
