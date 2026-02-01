#Pobranie tekstów piosenek z Hot16Challenge2
import lyricsgenius
import os
import re
import time
from requests.exceptions import Timeout, ReadTimeout
import shutil
import pandas as pd

# --- KONFIGURACJA ---
# Token powinien być ustawiony w zmiennej środowiskowej `GENIUS_API_TOKEN`.
# NIE zapisuj tokena bezpośrednio w kodzie ani w repozytorium.
TOKEN = os.getenv("GENIUS_API_TOKEN")
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

# Setup folderów
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# --- GENIUS SETUP (Poprawiony Timeout) ---
# Ustawiamy timeout na 60 sekund i 5 prób ponowienia
genius = lyricsgenius.Genius(TOKEN, timeout=60, retries=5)
genius.verbose = False
genius.remove_section_headers = True
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)", "Skit", "Intro", "Reaction"]

def get_artist_list():
    print(">>> 1. Pobieranie listy artystów z drzewka nominacji...")
    
    # Próbujemy 3 razy, jeśli wywali błąd timeout
    for attempt in range(3):
        try:
            # Szukamy konkretnie tej strony. To może potrwać, więc czekamy.
            print(f"   Próba połączenia nr {attempt+1}...")
            song = genius.search_song("Hot16Challenge2 - Artyści, Nominacje, Drzewko", "Rap Genius Polska")
            
            if not song:
                print("   Błąd: Genius zwrócił pusty wynik.")
                return []
            
            # Jeśli się udało, przerywamy pętlę prób i idziemy dalej
            break
            
        except (Timeout, ReadTimeout) as e:
            print(f"   [TIMEOUT] Serwer myśli za długo. Czekam 5s i ponawiam... ({e})")
            time.sleep(5)
            if attempt == 2:
                print("   [ERROR] Nie udało się pobrać listy artystów po 3 próbach.")
                # PLAN AWARYJNY: Jeśli API nie działa, zwracamy ręczną listę topowych artystów, żebyś mógł pracować dalej
                print("   -> Używam listy awaryjnej (TOP artyści).")
                return ["Taco Hemingway", "Mata", "Quebonafide", "Young Leosia", "Białas", "Bedoes", "Solar", "Żabson", "Kukon", "Szpaku", "O.S.T.R.", "Paluch", "Peja", "Sokół", "Tede", "Kizo", "Malik Montana", "Sobel", "Oki", "Otsochodzi", "Jan-rapowanie", "Guzior", "Reto", "Sarius", "Bonson", "KęKę", "Łona", "Dziarma", "Wdowa", "AdMa", "Ryfa Ri", "Guova", "Kara"]
    
    # Parsowanie tekstu drzewka
    print(">>> Parsowanie ksywek...")
    artists = set()
    lines = song.lyrics.split('\n')
    
    for line in lines:
        # Dzielimy linię typu "Taco -> Mata, Bedoes" na części
        parts = re.split(r'->|,|&| feat\. ', line)
        for p in parts:
            name = p.strip()
            name = re.sub(r'\[.*?\]', '', name) # usuwa [Tekst...]
            name = re.sub(r'\(.*?\)', '', name) # usuwa nawiasy
            # Filtrowanie śmieci
            if len(name) > 1 and "Rap Genius" not in name and "Challenge" not in name and "nomin" not in name.lower():
                artists.add(name)
    
    sorted_artists = sorted(list(artists))
    print(f">>> Znaleziono {len(sorted_artists)} ksywek.")
    return sorted_artists

def download_lyrics(artist_list):
    print(f">>> 2. Rozpoczynam pobieranie tekstów do: {DATA_DIR}")
    
    total = len(artist_list)
    for i, artist in enumerate(artist_list):
        # Bezpieczna nazwa pliku
        safe_name = re.sub(r'[\\/*?:"<>|]', "", artist).strip()
        filepath = os.path.join(DATA_DIR, f"{safe_name}.txt")

        if os.path.exists(filepath):
            print(f"[{i+1}/{total}] {artist} - Już pobrane (SKIP)")
            continue

        print(f"[{i+1}/{total}] Pobieram: {artist}...")
        try:
            # Szukamy konkretnie hot16
            song = genius.search_song("Hot16Challenge2", artist)
            
            if song and ("hot16" in song.title.lower() or "challenge" in song.title.lower()):
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"{song.title}\n{song.lyrics}")
                print(f"   -> OK")
            else:
                print(f"   -> Brak utworu Hot16")
            
            time.sleep(2) # Krótsza pauza, bo mamy lepszy timeout
            
        except Exception as e:
            print(f"   -> Błąd: {e}")
            time.sleep(2)

def sort_files_by_gender(data_dir='data/raw/', women_dir='data/women/', men_dir='data/men/', mapping_file='data/author_genders.csv', dry_run=True, auto_assign_unmatched=False):
    """
    Sortuje pliki używając pliku mapowania ksywek -> płeć.
    mapping_file CSV format: nickname,gender (M/F)
    dry_run: jeśli True, nie przenosi plików, tylko drukuje co by zrobił i zwraca raport.
    auto_assign_unmatched: jeśli True, używa prostych heurystyk, aby przypisać wszystkie niezmapowane pliki do M/F.
    Zapisuje listę niezmapowanych autorów do `data/unmatched.txt` i zapisuje wymuszone przypisania do `data/forced_assignments.csv`.
    """
    import csv

    # Wczytaj mapowanie (jeśli istnieje)
    mapping = {}
    if os.path.exists(mapping_file):
        with open(mapping_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                nick = row[0].strip()
                gender = row[1].strip().upper() if len(row) > 1 else ''
                if nick:
                    mapping[nick] = gender

    # Tworzenie katalogów
    os.makedirs(women_dir, exist_ok=True)
    os.makedirs(men_dir, exist_ok=True)

    moved = {'women': [], 'men': []}
    unmatched = []

    for filename in os.listdir(data_dir):
        author = filename.rsplit('.', 1)[0]
        gender = None

        # Najpierw dokładne dopasowanie
        if author in mapping and mapping[author] in ('M', 'F'):
            gender = mapping[author]
        else:
            # Dopasowanie po podciągu, case-insensitive
            for nick, g in mapping.items():
                if nick.lower() in author.lower() and g in ('M', 'F'):
                    gender = g
                    break

        if gender == 'F':
            moved['women'].append(filename)
            if not dry_run:
                shutil.move(os.path.join(data_dir, filename), os.path.join(women_dir, filename))
        elif gender == 'M':
            moved['men'].append(filename)
            if not dry_run:
                shutil.move(os.path.join(data_dir, filename), os.path.join(men_dir, filename))
        else:
            unmatched.append(filename)

    # Zapisz listę niezmapowanych
    os.makedirs(os.path.join(os.getcwd(), 'data'), exist_ok=True)
    with open('data/unmatched.txt', 'w', encoding='utf-8') as f:
        for u in unmatched:
            f.write(u + '\n')

    forced = []
    # Heurystyki przypisania dla niezmapowanych
    if auto_assign_unmatched and unmatched:
        male_exceptions = {'kuba'}  # przykładowe wyjątki męskich ksywek kończących się na 'a'
        for filename in list(unmatched):
            author = filename.rsplit('.', 1)[0]
            # Oczyść token (zostaw litery i polskie znaki)
            token = re.sub(r"[^A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż0-9]", "", author).lower()
            if token.endswith('a') and token not in male_exceptions:
                gender = 'F'
                dest = women_dir
            else:
                gender = 'M'
                dest = men_dir

            forced.append((filename, author, gender))
            if gender == 'F':
                moved['women'].append(filename)
            else:
                moved['men'].append(filename)

            if not dry_run:
                shutil.move(os.path.join(data_dir, filename), os.path.join(dest, filename))
            # usuń z listy niezmapowanych
            unmatched.remove(filename)

        # Zapisz wymuszone przypisania
        with open('data/forced_assignments.csv', 'w', encoding='utf-8') as f:
            f.write('filename,author,gender,method\n')
            for fn, au, g in forced:
                f.write(f"{fn},{au},{g},heuristic_ending_a\n")

    # Podsumowanie
    print(f"Sortowanie (dry_run={dry_run}, auto_assign_unmatched={auto_assign_unmatched}):\n  Women: {len(moved['women'])}\n  Men: {len(moved['men'])}\n  Unmatched: {len(unmatched)} (lista -> data/unmatched.txt)")
    if forced:
        print(f"  Forced assignments: {len(forced)} (lista -> data/forced_assignments.csv)")

    return moved, unmatched, forced


def create_verses_csv(source_dirs=None, output_csv='data/verses.csv', min_verse_chars=10):
    """
    Przetwarza wszystkie .txt w katalogach źródłowych i zapisuje każdy fragment (zwrotkę) jako osobny wiersz CSV.

    Kolumny: song_id (unikalny na piosenkę), author, song_title, verse_order, text, source_path, num_lines, char_count
    """
    if source_dirs is None:
        source_dirs = [os.path.join('data', 'women'), os.path.join('data', 'men'), os.path.join('data', 'raw')]

    rows = []
    song_id_counter = 1
    total_songs = 0

    for src in source_dirs:
        if not os.path.exists(src):
            continue
        for root, _, files in os.walk(src):
            for fn in sorted(files):
                if not fn.lower().endswith('.txt'):
                    continue
                path = os.path.join(root, fn)
                try:
                    with open(path, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                except Exception as e:
                    print(f"Nie można wczytać {path}: {e}")
                    continue

                total_songs += 1
                # Autor - pobieramy z nazwy pliku (bez rozszerzenia)
                author = fn.rsplit('.', 1)[0]

                # Spróbuj wyodrębnić tytuł: jeśli pierwsza nie-pusta linia wygląda jak tytuł
                lines = content.splitlines()
                first_nonempty = ''
                for L in lines:
                    if L.strip():
                        first_nonempty = L.strip()
                        break

                song_title = ''
                lyrics = content
                if first_nonempty and len(lines) > 1:
                    # heurystyka: jeśli pierwsza linia krótka i ma <=10 słów -> traktuj jako tytuł
                    if len(first_nonempty) <= 200 and len(first_nonempty.split()) <= 10:
                        # usuń tę linię z tekstu aby nie duplikować
                        rest = '\n'.join(lines[1:]).strip()
                        if rest:
                            song_title = first_nonempty
                            lyrics = rest

                # Usuń nagłówki w nawiasach typu [Chorus], [Refren] itp.
                cleaned = re.sub(r'(?m)^\s*\[.*?\]\s*$', '\n', lyrics)

                # Podziel na zwrotki - po jednej lub więcej pustych liniach
                parts = [p.strip() for p in re.split(r'\n\s*\n+', cleaned) if p.strip()]

                verse_order = 1
                for p in parts:
                    if len(p) < min_verse_chars:
                        continue
                    rows.append({
                        'song_id': song_id_counter,
                        'author': author,
                        'song_title': song_title,
                        'verse_order': verse_order,
                        'text': p,
                        'source_path': path,
                        'num_lines': p.count('\n') + 1,
                        'char_count': len(p)
                    })
                    verse_order += 1

                song_id_counter += 1

    # Zapis do CSV i DataFrame
    df = pd.DataFrame(rows, columns=['song_id', 'author', 'song_title', 'verse_order', 'text', 'source_path', 'num_lines', 'char_count'])
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False, encoding='utf-8')
    # Zapis binarny dla szybszego wczytywania
    df.to_pickle(output_csv.replace('.csv', '.pkl'))

    print(f"Utworzono {len(df)} zwrotek z {song_id_counter-1} piosenek -> {output_csv}")
    return df


if __name__ == "__main__":
    lista = get_artist_list()
    if lista:
        download_lyrics(lista)
        # Najpierw wykonujemy dry-run, żebyś mógł sprawdzić klasyfikację.
        # Gdy będziesz gotowy, uruchom z dry_run=False
        sort_files_by_gender(dry_run=True)
        # Stwórz CSV z pojedynczymi zwrotkami (bez rozróżnienia płci)
        df = create_verses_csv()
        print(f"Zapisano {len(df)} zwrotek do data/verses.csv i data/verses.pkl")