from bs4 import BeautifulSoup
import requests
import pandas as pd

author_quotes = {}

choice = input("If you want select page number, please write 1. If you want select several page, please write 2 : ")
if choice == '1':

    page = input("Input page number : ")
    url = f'http://quotes.toscrape.com/page/{page}/'

    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')

    quotes = soup.select('div.col-md-8 div.quote')

    for quote_block in quotes:
        author = quote_block.select_one('small.author').text.strip()
        saying = quote_block.select_one('span.text').text.strip()
        
        if author not in author_quotes:
            author_quotes[author] = []
        author_quotes[author].append(saying)

    for author, sayings in author_quotes.items():
        print(f"\n{author}:")
        for s in sayings:
            print(f"  - {s}")
            
    df = pd.DataFrame([(author, saying) for author, sayings in author_quotes.items() for saying in sayings])  # ✔
    df.columns = ['author', 'saying']  # ✔
    df.to_csv('quotes.csv', index=False)  # ✔

elif choice == '2':
    page_number = input('input number of page you want to scrape : ')
    page_number = int(page_number)

    for i in range(page_number):
        url = f'http://quotes.toscrape.com/page/{i+1}/'

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html,'html.parser')

        quotes = soup.select('div.col-md-8 div.quote')

        for quote_block in quotes:
            author = quote_block.select_one('small.author').text.strip()
            saying = quote_block.select_one('span.text').text.strip()
        
            if author not in author_quotes:
                author_quotes[author] = []
            author_quotes[author].append(saying)

    for author, sayings in author_quotes.items():
        print(f"\n{author}:")
        for s in sayings:
            print(f"  - {s}")
            
    df = pd.DataFrame([(author, saying) for author, sayings in author_quotes.items() for saying in sayings])  # ✔
    df.columns = ['author', 'saying']  # ✔
    df.to_csv('quotes.csv', index=False)  # ✔
