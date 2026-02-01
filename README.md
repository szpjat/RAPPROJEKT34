# RAPPROJEKT34

_Reproducible Analytical Pipeline - Projekt 34_

## 📋 Opis projektu

Ten projekt implementuje pipeline analityczny zgodny z najlepszymi praktykami:
- ✅ Kod w kontroli wersji (Git)
- ✅ Zarządzanie zależnościami
- ✅ Bezpieczne zarządzanie sekretami (zmienne środowiskowe)
- ✅ Czyste środowisko robocze
- ✅ Dokumentacja i reprodukowalność

## 📁 Struktura projektu

```
RAPPROJEKT34/
├── data/               # Dane projektu (wykluczone z repo)
│   ├── raw/           # Surowe dane (nie commitowane)
│   ├── processed/     # Przetworzone dane
│   └── README.md      # Opis danych
├── notebooks/         # Jupyter notebooks do analizy
├── src/               # Kod źródłowy projektu
├── tests/             # Testy jednostkowe
├── output/            # Wyniki analiz (nie commitowane)
├── .env.example       # Przykładowy plik zmiennych środowiskowych
├── .gitignore         # Pliki wykluczane z repozytorium
├── requirements.txt   # Zależności Python
└── README.md          # Ten plik
```

## 🚀 Rozpoczęcie pracy

### Wymagania wstępne

- Python 3.8+
- pip lub conda

### Instalacja

1. Sklonuj repozytorium:
```bash
git clone https://github.com/szpjat/RAPPROJEKT34.git
cd RAPPROJEKT34
```

2. Utwórz wirtualne środowisko:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate     # Windows
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

4. Skonfiguruj zmienne środowiskowe:
```bash
cp .env.example .env
# Edytuj plik .env i dodaj swoje klucze API
```

## 🔐 Bezpieczeństwo

- **Nigdy nie commituj** tokenów, kluczy API ani haseł
- Wszystkie sekrety są przechowywane w zmiennych środowiskowych (plik `.env`)
- Plik `.env` jest wykluczony z repozytorium przez `.gitignore`
- Używaj pliku `.env.example` jako szablonu (bez rzeczywistych wartości)

## 📊 Użycie

Uruchom główny notebook:
```bash
jupyter notebook notebooks/
```

Uruchom skrypty analizy:
```bash
python src/main.py
```

## 🧪 Testowanie

```bash
pytest tests/
```

## 📝 Dobre praktyki

✅ **Repozytorium jest zgodne z najlepszymi praktykami:**
- Brak śmieci ani niepotrzebnych plików
- `.gitignore` poprawnie wyklucza środowiska, cache i dane surowe
- README.md aktualny i zgodny z zawartością repo
- Tokeny i klucze API tylko z ENV
- Wszystkie notebooki i dane na miejscu

## 🤝 Współpraca

1. Utwórz branch dla swojej funkcjonalności
2. Commituj zmiany z czytelnymi komunikatami
3. Otwórz Pull Request

## 📄 Licencja

MIT License - zobacz plik [LICENSE](LICENSE)
