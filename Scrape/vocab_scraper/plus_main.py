from bs4 import BeautifulSoup
import requests
import time
import random
import string
import os
import pandas as pd
from util import translate_sentences



text_url = []
sentences = []
vocab = []
dictionary = {}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36'
}

    
word_url = 'https://en.openrussian.org/ru/'
base_url = 'https://lingua.com/russian/reading/'
response = requests.get(base_url, headers=headers)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

def normalize(word):
    return word.strip(string.punctuation + "—«»„“").lower()

def vocab_collector():
    href_blocks = soup.select('div.panel.panel-exercises ul.exercise-list')
    for block in href_blocks:
        links = block.select('a.reading-link')
        for link in links:
            href = link.get('href')
            if href:
                text_url.append(href)
    
    print("Collected links:", text_url)

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
                #translate_sentences(sentences)

                words = txt.split()
                for word in words:
                    cleaned = normalize(word)
                    if cleaned and cleaned not in vocab:
                        vocab.append(cleaned)

            time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"Error fetching {full_url}: {e}")

    print("\nSample Sentences:")
    for s in sentences[:3]:
        print("-", s)

    print(f"\nTotal unique vocab words: {len(vocab)}")
    print("Sample vocab:", vocab[:30])

def vocab_translator():
    csv_file = 'translated_vocab.csv'
#_________________________________________________________________________________________________________
    if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            dictionary.update({row['word']: eval(row['translations']) for _, row in df.iterrows()})
            print(f"Loaded {len(dictionary)} words from CSV.")
#__________________________________________________________________________________________________________-

    for i in vocab:
        if i in dictionary:   #______________________
            print(f"Already translated: {i}")
            continue          #_____________________________
        full_words_url = word_url + i
        print(f"\nFetching: {full_words_url}")

        try:
            response = requests.get(full_words_url,headers=headers)
            soup3 = BeautifulSoup(response.text,'html.parser')
            tl_texts = [t.text for t in soup3.select('p.tl')]

            if tl_texts:
                print("Translation:", tl_texts)
                dictionary[i] = tl_texts
                pd.DataFrame([{'word': i, 'translations': tl_texts}]).to_csv(
                    csv_file,
                    mode='a',
                    header=not os.path.exists(csv_file),
                    index=False
                )

            else:
                print("No translation found.")

            time.sleep(random.uniform(1, 2))

        except Exception as e:
            print(f"Error scraping {full_words_url} : {e}")

vocab_collector()
vocab_translator()




#ToDo : do not add the word when there is no translation!  _OK
#2 : create dictionary via pandas _OK
#3 : translate per page using selenium and create dictionary again.