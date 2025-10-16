from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

def scrape_rightmove(url, max_items=50):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(3)

    results = []
    cards = driver.find_elements(By.CSS_SELECTOR, ".commercial-result, .propertyCard")
    for idx, c in enumerate(cards):
        if idx >= max_items: break
        try:
            name = c.find_element(By.CSS_SELECTOR, ".propertyCard-title").text
        except:
            name = c.text[:60]
        try:
            address = c.find_element(By.CSS_SELECTOR, ".propertyCard-address").text
        except:
            address = ""
        try:
            price = c.find_element(By.CSS_SELECTOR, ".propertyCard-priceValue").text
        except:
            price = ""
        try:
            features = c.find_element(By.CSS_SELECTOR, ".propertyCard-contacts").text
        except:
            features = ""
        results.append({
            "Name": name, "Address": address,
            "Features": features, "Prices or Rates": price, "Other Relevant Information": ""
        })

    driver.quit()
    return pd.DataFrame(results)
