"""
Testy dla modułu konfiguracji
"""

import pytest
from pathlib import Path
import sys

# Dodaj src do ścieżki
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config import PROJECT_ROOT, DATA_DIR, RAW_DATA_DIR


def test_project_root_exists():
    """Sprawdź czy katalog główny projektu istnieje"""
    assert PROJECT_ROOT.exists()
    assert PROJECT_ROOT.is_dir()


def test_data_directories():
    """Sprawdź czy katalogi danych istnieją"""
    assert DATA_DIR.exists()
    assert RAW_DATA_DIR.exists()


def test_project_structure():
    """Sprawdź czy podstawowe katalogi projektu istnieją"""
    assert (PROJECT_ROOT / 'src').exists()
    assert (PROJECT_ROOT / 'tests').exists()
    assert (PROJECT_ROOT / 'notebooks').exists()
    assert (PROJECT_ROOT / 'data').exists()
