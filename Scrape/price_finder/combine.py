from replace_am import amazon_scraper
from replace import rakuten_scraper

price_bucket = []

keyword = input("Enter the product to search on Amazon and Rakuten: ")

def main():
    lowest_price_amazon = amazon_scraper(keyword)
    if lowest_price_amazon is not None:
        print(f"The lowest price on Amazon is: ${lowest_price_amazon}")
        lowest_price_amazon = str(lowest_price_amazon)
        price_bucket.append('$' + lowest_price_amazon)
    else:
        print("No valid prices were found on Amazon.")

    lowest_price_rakuten = rakuten_scraper(keyword)
    if lowest_price_rakuten is not None:
        print(f"The lowest price on Rakuten is: ¥{lowest_price_rakuten}")
        lowest_price_rakuten = str(lowest_price_rakuten)
        price_bucket.append('¥' + lowest_price_rakuten)
    else:
        print("No valid prices were found on Rakuten.")

if __name__ == "__main__":
    main()

print("Prices collected:", price_bucket)