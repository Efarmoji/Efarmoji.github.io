from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# List of user agents to rotate
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121 Safari/537.36"
]

# Set Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f"user-agent={random.choice(user_agents)}")

# Start the browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Search keyword
keyword = ''
def rakuten_scraper():
    price_map = {}
    keyword = input('input keyword : ')
    url = f"https://search.rakuten.co.jp/search/mall/{keyword}/"

    # Open URL
    driver.get(url)
    time.sleep(5)

    # Scroll to bottom to load more content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Get products
    products = driver.find_elements(By.CSS_SELECTOR, 'div.searchResults div.dui-card.searchresultitem.overlay-control-wrapper--3KBO0.title-control-wrapper--1rzvX')

    # Extract and print data
    for idx, product in enumerate(products[:10]):
        try:
            title = product.find_element(By.CSS_SELECTOR, 'h2.title-link-wrapper--25--s.title-link-wrapper-grid--hGeiw').text
        except:
            title = f"{idx} : N/A"

        try:
            price = product.find_element(By.CSS_SELECTOR, 'div.price-wrapper--10ccL').text
        except:
            price = f"{idx} : N/A"

        print(f'{title} : {price}')

        if title not in price_map:
            price_map[title] = []
        price_map[title].append(price)

    # Get the first price to initialize comparison
    first_prices = next(iter(price_map.values()))
    price = int(first_prices[0].replace(",", "").replace("円", ""))

    for prices in price_map.values():
        for p in prices:
            try:
                p_int = int(p.replace(",", "").replace("¥", ""))
                if p_int < price:
                    price = p_int
            except ValueError:
                continue  # skip if not a number

    print(f"The most reasonable one is: {price}")



    # Close browser
    driver.quit()
    #span class="a-offscreen"
rakuten_scraper()