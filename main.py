import requests
from bs4 import BeautifulSoup
import datetime
import os
import json

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

def get_product_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select('.product-name a')
    return ["https://crossjeans.pl" + link['href'] for link in links if link.has_attr('href')]

def load_previous_links():
    if os.path.exists('products.json'):
        with open('products.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_current_links(data):
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    today = datetime.date.today().isoformat()
    previous = load_previous_links()
    current = {}
    new = {}

    for category, url in URLS.items():
        links = get_product_links(url)
        current[category] = links
        old_links = previous.get(category, [])
        new_links = [link for link in links if link not in old_links]
        if new_links:
            new[category] = new_links

    save_current_links(current)

    with open(f"nowe_produkty_{today}.txt", "w", encoding="utf-8") as f:
        if not new:
            f.write("Brak nowych produktów.")
        else:
            for category, links in new.items():
                f.write(f"{category}:\n")
                for link in links:
                    f.write(f"  - {link}\n")
                f.write("\n")

if __name__ == "__main__":
    main()
