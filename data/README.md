# Dane projektu

## Struktura

### `raw/`
Surowe, nieprzetworzone dane. **Katalog nie jest commitowany do repozytorium.**

- Pobrane z zewnętrznych źródeł
- Niemodyfikowane
- Przechowywane lokalnie lub w chmurze

### `processed/`
Dane przetworzone i przygotowane do analizy.

- Oczyszczone dane
- Dane po transformacjach
- Gotowe do użycia w notebookach i skryptach

## Uwagi

⚠️ **Nie commituj dużych plików danych do repozytorium Git.**

Zamiast tego:
- Użyj `.gitignore` do wykluczenia katalogów z danymi surowymi
- Dodaj instrukcje pobierania danych w dokumentacji
- Rozważ użycie DVC (Data Version Control) dla dużych zbiorów danych
- Lub przechowuj dane w chmurze (S3, Google Cloud Storage, etc.)

## Źródła danych

Opisz tutaj źródła danych używanych w projekcie:
- URL lub API do pobrania
- Metoda pozyskania
- Format danych
- Licencja
