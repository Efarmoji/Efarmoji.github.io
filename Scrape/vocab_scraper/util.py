# uril.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os
import urllib.parse

def translate_sentences(sentences, output_csv='translated_sentences.csv', source_lang='ru', target_lang='en'):
    # Load already translated sentences
    already_translated = set()
    if os.path.exists(output_csv):
        df_existing = pd.read_csv(output_csv)
        already_translated = set(df_existing['sentence'].dropna().tolist())

    # Set up headless browser
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    new_translations = []

    for sentence in sentences:
        if sentence in already_translated:
            print(f"⏭️ Skipping (already translated): {sentence}")
            continue

        try:
            print(f"🌐 Translating: {sentence}")
            encoded_sentence = urllib.parse.quote(sentence)
            url = f"https://lingva.ml/{source_lang}/{target_lang}/{encoded_sentence}"
            driver.get(url)

            wait = WebDriverWait(driver, 10)
            result_elem = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div.chakra-stack div.translation')
            ))

            translation = result_elem.text.strip()
            print(f"✅ {translation}")
            new_translations.append({'sentence': sentence, 'translation': translation})

        except Exception as e:
            print(f"❌ Error translating sentence: {e}")
            new_translations.append({'sentence': sentence, 'translation': 'ERROR'})

        time.sleep(2)

    driver.quit()

    # Save to CSV
    if new_translations:
        df_new = pd.DataFrame(new_translations)
        if os.path.exists(output_csv):
            df_new.to_csv(output_csv, mode='a', header=False, index=False)
        else:
            df_new.to_csv(output_csv, index=False)

        print(f"\n📁 Saved {len(df_new)} new translations to {output_csv}")
    else:
        print("\n📭 No new translations were needed.")

# Example usage
if __name__ == "__main__":
    sample_sentences = [
        "У меня большая семья из шести человек: я, мама, папа, старшая сестра, бабушка и дедушка. Мы живем все вместе с собакой Бимом и кошкой Муркой в большом доме в деревне. Мой папа встает раньше всех, потому что ему рано на работу. Он работает доктором. Обычно бабушка готовит нам завтрак. Я обожаю овсяную кашу, а моя сестра Аня – блины.",
        "После завтрака мы собираемся и идем в школу. Моя сестра учится в пятом классе, а я – во втором. Мы любим учиться и играть с друзьями. Больше всего я люблю географию. Когда мы приходим домой из школы, мы смотрим телевизор, а потом ужинаем и делаем уроки. Иногда мы помогаем бабушке и маме в огороде, где они выращивают овощи и фрукты."
    ]
    translate_sentences(sample_sentences)
