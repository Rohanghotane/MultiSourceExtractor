import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_graypoint(url):
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    listings = []

    
    cards = soup.select(".property") or soup.select(".listing, .property-card")
    for c in cards:
        name = c.select_one(".title, h2") and c.select_one(".title, h2").get_text(strip=True) or ""
        address = c.select_one(".address") and c.select_one(".address").get_text(strip=True) or ""
        features = ", ".join([li.get_text(strip=True) for li in c.select(".features li")]) if c.select(".features li") else ""
        price = c.select_one(".price") and c.select_one(".price").get_text(strip=True) or ""
        other = c.select_one(".description") and c.select_one(".description").get_text(strip=True) or ""
        listings.append({
            "Name": name, "Address": address, "Features": features,
            "Prices or Rates": price, "Other Relevant Information": other, "SourceURL": url
        })

    return pd.DataFrame(listings)
