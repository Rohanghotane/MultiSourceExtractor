from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

def scrape_amazon_table_fans(search="table fan", max_results=20):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    base = "https://www.amazon.in"
    driver.get(f"{base}/s?k={search.replace(' ', '+')}")
    time.sleep(3)

    items = []
    product_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-asin]")[:max_results]
    for card in product_cards:
        asin = card.get_attribute("data-asin")
        if not asin: continue
        try:
            title = card.find_element(By.CSS_SELECTOR, "h2 a span").text
        except:
            title = ""
        try:
            price = card.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen").text
        except:
            price = ""
        product_url = None
        try:
            anchor = card.find_element(By.CSS_SELECTOR, "h2 a")
            product_url = anchor.get_attribute("href")
        except:
            pass

        # Visit product page for detailed info
        dims = weight = manufacturer = warranty = features = color = ""
        if product_url:
            driver.get(product_url)
            time.sleep(2)
            # parse product details table
            try:
                details = driver.find_elements(By.CSS_SELECTOR, "#productDetails_techSpec_section_1 tr")
                for r in details:
                    key = r.find_element(By.TAG_NAME, "th").text.strip()
                    val = r.find_element(By.TAG_NAME, "td").text.strip()
                    if "Weight" in key: weight = val
                    if "Dimensions" in key: dims = val
                    if "Manufacturer" in key: manufacturer = val
                    if "Warranty" in key: warranty = val
                    if "Colour" in key or "Color" in key: color = val
            except:
                # alternate selectors
                pass

        items.append({
            "Product Name": title, "Product Code or SKU ID": asin,
            "Price": price, "Dimensions": dims, "Weight": weight,
            "Manufacturer Name": manufacturer, "Warranty": warranty,
            "Features": features, "Color": color, "Product URL": product_url
        })

        # go back to search results
        driver.back()
        time.sleep(1)

    driver.quit()
    return pd.DataFrame(items)
