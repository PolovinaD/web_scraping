from bs4 import BeautifulSoup
import requests
import csv

url = "https://www.bookdepository.com/search?searchTerm=python&cathegory=1708&page=1"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

items = doc.find_all(["div"], class_ = "item-info")

books = []
fieldnames = ["Title", "Author", "Rating", "Format", "Price"]

for item in items:
    title = item.find(["h3"], class_ = "title").a.string.strip()
    author = item.find(["p"], class_ = "author").find(["span"], itemprop = "name").string
    format = item.find(["p"], class_ = "format").string.strip()

    price = item.find(["p"], class_ = "price").text.strip().split(" ")[0]
    temp_price = list(price)
    for i in range(len(temp_price)):
        if temp_price[i] == ',':
            temp_price[i] = '.'
            break
    
    price = "".join(temp_price)
    price += "€"

    full_stars = item.find(["div"], class_ = "stars").find_all(["span"], class_ = "star full-star")
    half_stars = item.find(["div"], class_ = "stars").find(["span"], class_ = "star half-star")
    
    rating = len(full_stars)
    if half_stars != None:
        rating += 0.5

    book = {'Title': title,
    'Author': author,
    'Rating': rating,
    'Format': format,
    'Price' : price}
    
    books.append(book)

with open("books.csv", "w",encoding='UTF8') as file:
    writer = csv.DictWriter(file, quoting = csv.QUOTE_NONNUMERIC, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(books)