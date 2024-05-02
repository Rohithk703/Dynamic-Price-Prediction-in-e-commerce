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


csv_filename = 'flipkart_gaming_laptops(1).csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['product_name', 'brand_name', 'price', 'mrp', 'offer'])

for page_num in range(1, 24):
    retries = 10
    while retries > 0:
        try:
            browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

            URL = f'https://www.flipkart.com/search?q=gaming+laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_13_na_na_na&as-pos=1&as-type=RECENT&suggestionId=gaming+laptop%7CLaptops&requestId=05b892e9-0e96-494c-b879-e25e56fb8bd8&as-backfill=on&page={page_num}'

            browser.get(URL)
            time.sleep(3)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            browser.close()

            tiles = soup.find_all('div', attrs={'class': 'yKfJKb row'})

            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                for tile in tiles:
                    product_name = tile.find('div', attrs={'class': 'KzDlHZ'}).text.strip()
                    brand_name = product_name.split()[0]
                    price = preprocess_price(tile.find('div', attrs={'class': 'Nx9bqj _4b5DiR'}).text.strip())
                    mrp = preprocess_price(tile.find('div', attrs={'class': 'yRaY8j ZYYwLA'}).text.strip())
                    offer = (100 * (mrp - price)) / price
                    writer.writerow([product_name, brand_name, price, mrp, offer])
            break

        except Exception as e:
            print(f'An error occurred: {e}. Retrying...')
            retries -= 1
            time.sleep(1)
    print(f'{page_num} completed')




