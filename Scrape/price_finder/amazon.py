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

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

keyword = ''
# Search keyword
def amazon_scraper():
    url = f"https://www.amazon.com/s?k={keyword}"

    # Open URL
    driver.get(url)
    time.sleep(5)

    # Scroll to bottom to load more content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Get products
    products = driver.find_elements(By.CSS_SELECTOR, 'div.s-main-slot div.s-result-item')

    # Extract and print data
    for product in products[:10]:
        try:
            title = product.find_element(By.CSS_SELECTOR, 'h2 span').text
        except:
            title = "N/A"

        try:
            price = product.find_element(By.CSS_SELECTOR, 'span.a-offscreen').text
        except:
            price = "N/A"

        print(f"Title: {title}\nPrice: {price}\n")

    # Close browser
    driver.quit()
    #span class="a-offscreen"