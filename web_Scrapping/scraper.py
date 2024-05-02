from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
import time
import csv


def preprocess_mrp(string):
    unique_string = string[:len(string) // 2]
    number = float(unique_string.replace('₹', '').replace(',', ''))
    return number


def preprocess_price(string):
    number = float(string.replace('₹', '').replace(',', ''))
    return number


def preprocess_purchase(string):
    number = int(string.replace(',', ''))
    return number


csv_filename = 'amazon_gaming_laptops(3).csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['product_name', 'brand_name', 'price', 'mrp', 'offer'])

for page_num in range(1, 21):
    retries = 10
    while retries > 0:
        try:
            browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

            URL = f'https://www.amazon.in/s?k=gaming+laptop&page={page_num}&qid=1714548442&xpid=gpAUjutbWVa-6&ref=sr_pg_{page_num}'

            browser.get(URL)
            time.sleep(3)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            browser.close()

            tiles = soup.find_all("div", attrs={'class': 'a-section a-spacing-small a-spacing-top-small'})

            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                for tile in tiles[1:]:
                    product_name = tile.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
                    brand_name = product_name.split()[0]
                    price = preprocess_price(tile.find('span', attrs={'class': 'a-price-whole'}).text.strip())
                    mrp = preprocess_mrp(tile.find('span', attrs={'class': 'a-price a-text-price'}).text.strip())
                    offer = (100 * (mrp - price)) / price
                    writer.writerow([product_name, brand_name, price, mrp, offer])

            break
        except Exception as e:
            print(f"An Error occurred: {e}. Retrying...")
            retries -= 1
            time.sleep(1)
    print(f'{page_num} completed')

