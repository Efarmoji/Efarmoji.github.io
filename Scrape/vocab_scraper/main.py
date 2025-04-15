from bs4 import BeautifulSoup
import requests
import time
import random

text_url = []
sentences = []
vocab = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36'
}


base_url = 'https://lingua.com/russian/reading/'
response = requests.get(base_url,headers=headers)
html = response.text
soup = BeautifulSoup(html,'html.parser')

def vocab_collector():
    href_blocks = soup.select('div.panel.panel-exercises ul.exercise-list')
    for block in href_blocks:
        links = block.select('a.reading-link')
        for link in links:
            href = link.get('href')
            if href:
                text_url.append(href)
    
    print(text_url)

    for i in text_url:
        full_url = base_url + i
        print(f"\nFetching: {full_url}")

        try:
            response = requests.get(full_url, headers=headers)
            soup2 = BeautifulSoup(response.text, 'html.parser')

            texts = soup2.select('div.fifty_left p')
            for p in texts:
                txt = p.text.strip()
                sentences.append(txt)

            time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"Error fetching {full_url}: {e}")
    print(sentences)

    

vocab_collector()