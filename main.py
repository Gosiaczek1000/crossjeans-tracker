import requests
from bs4 import BeautifulSoup
import datetime
import os
import json

# Lista kategorii i odpowiadających im URLi
URLS = {
    'Jeansy damskie': 'https://crossjeans.pl/ona/jeansy-damskie?limit=0',
    'Spodnie damskie': 'https://crossjeans.pl/ona/spodnie-damskie?limit=0',
    'Odzież damska': 'https://crossjeans.pl/ona/odziez-damska?limit=0',
    'Buty damskie': 'https://crossjeans.pl/ona/buty-damskie?limit=0',
    'Akcesoria damskie': 'https://crossjeans.pl/ona/akcesoria-damskie?limit=0',
    'Basic damski': 'https://crossjeans.pl/ona/basic-damski?limit=0',
    'Komplety damskie': 'https://crossjeans.pl/ona/komplety-damskie?limit=0',
    'Jeansy męskie': 'https://crossjeans.pl/on/jeansy-meskie?limit=0',
    'Spodnie męskie': 'https://crossjeans.pl/on/spodnie-meskie?limit=0',
    'Buty męskie': 'https://crossjeans.pl/on/buty-meskie?limit=0',
    'Akcesoria męskie': 'https://crossjeans.pl/on/akcesoria-meskie?limit=0',
    'Basic męski': 'https://crossjeans.pl/on/basic-meski?limit=0',
    'Nowości damskie': 'https://crossjeans.pl/lp-nowosci-damskie?limit=0',
    'Nowości męskie': 'https://crossjeans.pl/lp-nowosci-meskie?limit=0',
    'Odzież męska str. 1': 'https://crossjeans.pl/on/odziez-meska?limit=100',
    'Odzież męska str. 2': 'https://crossjeans.pl/on/odziez-meska?limit=100&page=2',
    'Odzież męska str. 3': 'https://crossjeans.pl/on/odziez-meska?limit=100&page=3',
    'Odzież męska str. 4': 'https://crossjeans.pl/on/odziez-meska?limit=100&page=4',
    'Odzież męska str. 5': 'https://crossjeans.pl/on/odziez-meska?limit=100&page=5',
}

# Pobiera nazwy produktów z danej strony
def get_products(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.select('.product-name a')
    return [p.text.strip() for p in products]

# Wczytuje dane z poprzedniego dnia (jeśli istnieją)
def load_previous_products():
    if not os.path.exists("products.json"):
        return {}
    with open("products.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Zapisuje aktualną listę produktów
def save_current_products(data):
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Główna logika programu
def main():
    previous = load_previous_products()
    current = {}
    new_products = {}

    for category, url in URLS.items():
        products = get_products(url)
        current[category] = products
        old = previous.get(category, [])
        new_items = [p for p in products if p not in old]
        if new_items:
            new_products[category] = new_items

    save_current_products(current)

    today = datetime.date.today().isoformat()
    with open(f"nowe_produkty_{today}.txt", "w", encoding="utf-8") as f:
        if not new_products:
            f.write("Brak nowych produktów.")
        else:
            for category, items in new_products.items():
                f.write(f"{category}:\n")
                for item in items:
                    f.write(f"  - {item}\n")
                f.write("\n")

# Uruchomienie skryptu
if __name__ == "__main__":
    main()
