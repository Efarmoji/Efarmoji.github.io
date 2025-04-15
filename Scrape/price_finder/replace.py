from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import re


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121 Safari/537.36"
]

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f"user-agent={random.choice(user_agents)}")


def extract_price(text):
    text = text.replace(",", "")
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None

def rakuten_scraper(keyword):
    url = f"https://search.rakuten.co.jp/search/mall/{keyword}/"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    
    driver.get(url)
    time.sleep(5)

    products = driver.find_elements(By.CSS_SELECTOR, 'div.searchResults div.dui-card.searchresultitem.overlay-control-wrapper--3KBO0.title-control-wrapper--1rzvX')

    prices = []

    for product in products[:10]:
        try:
            title = product.find_element(By.CSS_SELECTOR, 'h2.title-link-wrapper--25--s.title-link-wrapper-grid--hGeiw').text
        except:
            title = "N/A"

        try:
            price_text = product.find_element(By.CSS_SELECTOR, 'div.price-wrapper--10ccL').text


        except:
            price_text = "N/A"

        price = extract_price(price_text)
        if price is not None:
            prices.append(price)
        
        print(f"Title : {title}\nPrice: {price_text}\n")

    driver.quit()

    if prices:
        return min(prices)
    else:
        return None