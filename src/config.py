"""
Konfiguracja projektu
Pobiera zmienne środowiskowe z pliku .env
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Ścieżka do głównego katalogu projektu
PROJECT_ROOT = Path(__file__).parent.parent

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv(PROJECT_ROOT / '.env')

# Pobierz zmienne środowiskowe
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
DATABASE_URL = os.getenv('DATABASE_URL')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Ścieżki do katalogów
DATA_DIR = PROJECT_ROOT / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
OUTPUT_DIR = PROJECT_ROOT / 'output'
NOTEBOOKS_DIR = PROJECT_ROOT / 'notebooks'

# Upewnij się, że katalogi istnieją
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, OUTPUT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
