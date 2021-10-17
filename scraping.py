from os import system
from bs4 import BeautifulSoup
import requests
import csv

initial_url = "https://www.bookdepository.com/search?searchTerm=python&cathegory=1708&page=1"
result = requests.get(initial_url)
doc = BeautifulSoup(result.text, "html.parser")

items_count = doc.find(["span"], class_ = "search-count").string
items_count = int("".join(items_count.split(',')))
max_pages = int(items_count/30) + 1

pages = 1
try:
    pages_input = int(input("Type in a positive number of pages you want to scrape (default is {}, max is {}): ".format(pages, max_pages)))
except:
    print("Wrong input, must be an integer!")
    exit()

if pages_input != None and pages_input > 0:
    if pages_input > max_pages:
        pages = max_pages
    else:
        pages = pages_input

books = []
fieldnames = ["Title", "Author", "Rating", "Format", "Price"]

for page in range(1, pages + 1):
    url = f"https://www.bookdepository.com/search?searchTerm=python&cathegory=1708&page={page}"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    items = doc.find_all(["div"], class_ = "item-info")

    for item in items:
        title = item.find(["h3"], class_ = "title").a.string.strip()
        author = item.find(["p"], class_ = "author").find(["span"], itemprop = "name").string
        format = item.find(["p"], class_ = "format").string.strip()

        price = item.find(["p"], class_ = "price")
        if price != None:
            price = price.text.strip().split(" ")[0]
            temp_price = list(price)
            for i in range(len(temp_price)):
                if temp_price[i] == ',':
                    temp_price[i] = '.'
                    break
            
            price = "".join(temp_price)
            price += "€"

        stars = item.find(["div"], class_ = "stars")
        if stars != None:
            full_stars = stars.find_all(["span"], class_ = "star full-star")
            half_stars = stars.find(["span"], class_ = "star half-star")
            
            rating = len(full_stars)
            if half_stars != None:
                rating += 0.5
        else:
            rating = None

        book = {'Title': title,
        'Author': author,
        'Rating': rating,
        'Format': format,
        'Price' : price}
        
        books.append(book)

with open("books.csv", "w", encoding='UTF8') as file:
    writer = csv.DictWriter(file, quoting = csv.QUOTE_NONNUMERIC, fieldnames = fieldnames)
    writer.writeheader()
    writer.writerows(books)