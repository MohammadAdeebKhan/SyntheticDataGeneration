import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "Mysql123"),
    "port": int(os.getenv("DB_PORT", 3306))
}

DOMAINS = ['ecommerce', 'fintech', 'healthcare', 'education', 'logistics', 'hr']

DATA_GENERATION_CONFIG = {
    "batch_size": 500,
    "max_rows": 10000,
    "min_rows": 10
}

STREAMLIT_CONFIG = {
    "page_title": "Data Generation Platform",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}
