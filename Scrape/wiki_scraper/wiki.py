from bs4 import BeautifulSoup
import requests

scraper = input('Input search term : ')
if scraper:
    text_for_scraper = scraper.lower()
    text_for_scraper = text_for_scraper.replace(' ','_')

url = f'https://en.wikipedia.org/wiki/{text_for_scraper}'
print(url)

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html,'html.parser')

title = soup.find('span',class_='mw-page-title-main')
print(title.text)

print("Reached content extraction step")

print('here, content skipped')

print("Looking for first meaningful paragraph...")

paragraphs = soup.select("div.mw-content-ltr.mw-parser-output > p")

for idx, p in enumerate(paragraphs):
    text = p.get_text(separator=' ', strip=True)
    if text:
        print(f"\nFound content in paragraph #{idx+1}:")
        print(text)
        print('______________________________________________________')
else:
    print("No meaningful content found.")

#<span class="mw-page-title-main">Fast Fourier transform</span>
#class="mw-content-ltr mw-parser-output"