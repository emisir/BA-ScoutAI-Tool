import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from tqdm import tqdm
import os

# Installieren Sie automatisch die passende Version von ChromeDriver
chromedriver_autoinstaller.install()

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Führen Sie Chrome im Headless-Modus aus
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Benutzer nach Ligen und Jahren fragen
leagues = input("Geben Sie die Ligen ein, getrennt durch Kommas (z.B. 'bundesliga, 2-bundesliga, 3-liga'): ").lower().split(', ')
years = input("Geben Sie die Jahre ein, getrennt durch Kommas (z.B. '2021-2022, 2022-2023'): ").split(', ')

# URL basierend auf Benutzereingaben erstellen
base_url = "https://fbref.com/en/comps/"

league_mapping = {
        'premier-league': '9',
        'la-liga': '12',
        'bundesliga': '20',
        'serie-a': '11',
        'ligue-1': '13',
        'eredivisie': '23',
        'primeira-liga': '32',
        '2-bundesliga': '33',
        '3-liga': '59',
        'championship': '10',
        'serie-b': '15',
        'ligue-2': '17',
        'major-league-soccer': '19',
        'a-league': '57',
        'super-lig': '58',
        'russian-premier-league': '29',
        'jupiler-pro-league': '37',
        'süper-lig': '58',
        'pro-league': '23'
}

for league in leagues:
    for year in years:
        league_id = league_mapping.get(league)
        
        if not league_id:
            print(f"Liga '{league}' wird nicht unterstützt.")
            continue

        url = f"{base_url}{league_id}/{year}/stats/{year}-{league.capitalize()}-Stats"

        print(f"Öffne URL: {url}")
        # Webseite öffnen
        driver.get(url)

        # Warten, bis die Tabelle geladen ist
        wait = WebDriverWait(driver, 10)
        table = wait.until(EC.presence_of_element_located((By.ID, "stats_standard")))

        # Tabelle finden
        table = driver.find_element(By.ID, "stats_standard")

        # Tabellenkopf extrahieren
        header = table.find_element(By.TAG_NAME, "thead")
        header_rows = header.find_elements(By.TAG_NAME, "tr")[1]

        # Header-Liste vorbereiten
        headers = []
        for th in header_rows.find_elements(By.TAG_NAME, "th"):
            header_text = th.text
            headers.append(header_text)

        headers = headers[1:-1]

        # # Überprüfen der Header
        # print(f"Headers: {headers}")
        print(f"Number of headers: {len(headers)}")

        # Tabellenkörper extrahieren
        body = table.find_element(By.TAG_NAME, "tbody")
        rows = body.find_elements(By.TAG_NAME, "tr")

        # Daten aus jeder Zeile extrahieren mit Fortschrittsanzeige
        data = []
        for row in tqdm(rows, desc=f"Extrahiere Daten aus Zeilen für {league} {year}"):
            cells = row.find_elements(By.TAG_NAME, "td")
            cell_data = [cell.text for cell in cells]
            data.append(cell_data)

        data = [row[:-1] for row in data]
        print(f"Number of cols: {len(data)}")

        # Daten in Pandas DataFrame umwandeln und Anzahl der Spalten prüfen
        df = pd.DataFrame(data)
        if df.shape[1] == len(headers):
            df.columns = headers
        else:
            print(f"Mismatch between number of headers ({len(headers)}) and columns ({df.shape[1]})")

        # Erstellen des Ausgabeverzeichnisses, falls es nicht existiert
        output_dir = "./output"
        os.makedirs(output_dir, exist_ok=True)

        # DataFrame in eine CSV-Datei schreiben
        output_file = f'{output_dir}/{league}_stats_{year}.csv'
        df.to_csv(output_file, index=False)
        print(f"Daten wurden in '{output_file}' gespeichert")

# Schließen des Browsers
driver.quit()
