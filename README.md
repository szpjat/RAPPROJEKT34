
# ProjektFinal — analiza tekstów rapowych

Krótki opis
- Repozytorium zawiera oczyszczone zwrotki (CSV) oraz notebooki z analizą eksploracyjną i wizualizacjami.
- Główne pliki:
   - `glownaanaliza.ipynb` — analiza introspection, power, wykresy (scatter, typy narracji).
   - `zrozumienie_danych_fixed.ipynb` — dodatkowe analizy i wizualizacje.
   - `verses_cleaned_no_thanks_nom.csv` — dane wejściowe (zwrotki).
   - `data/verses.csv` — zwrotki w formacie CSV (główna tabela).
   - `README.md` — ten plik.

Wymagania

  pip install -r requirements.txt

Szybki start
1. Utwórz i aktywuj wirtualne środowisko (opcjonalnie):

   python -m venv .venv
   source .venv/bin/activate

2. Zainstaluj zależności:

   pip install -r requirements.txt

3. Uruchom Jupyter i otwórz notebooki:

   jupyter lab
   # lub
   jupyter notebook

4. W `glownaanaliza.ipynb` uruchamiaj komórki w kolejności od początku (najpierw wczytanie danych i budowa słownika `emo_dict`, potem komórki tworzące kolumny `introspection` i `power`, a na końcu wykresy).

Ustawienie tokena Genius API

   GENIUS_API_TOKEN=twój_token

- Alternatywnie eksportuj zmienną w terminalu przed uruchomieniem:

   export GENIUS_API_TOKEN='twój_token'


Uwaga o wykresie z medianami
- Komórka tworząca scatter automatycznie wylicza mediany `p_med` i `i_med`, więc nie wymaga wcześniejszego ręcznego ustawiania tych zmiennych. Jeśli napotkasz `NameError`, uruchom komórki przygotowujące kolumny (`introspection`, `power`) przed wykresem.

Dodatkowe skrypty
- `main.py` — pobieranie surowych tekstów (używa `lyricsgenius`).
- `scripts/build_from_raw.py` — buduje CSV z plików `data/raw/`.
- `scripts/clean_verses.py` — prostsze czyszczenie CSV bez pandas.

Kontakt
- Projekt lokalny — w razie problemów napisz w kodzie lub zostaw issue w repozytorium lokalnym.
