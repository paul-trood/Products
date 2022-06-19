import requests
from bs4 import BeautifulSoup

# URL for website thewhiskyexchange.com
baseurl = "https://www.thewhiskyexchange.com/"

# headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

# To iterate through multiple pages
product_links = []

for i in range(1): # change range for the number of pages
    r = requests.get(f"https://www.thewhiskyexchange.com/c/540/taiwanese-whisky?pg={i}") # change link if neccessary
    # pip install lxml 
    soup = BeautifulSoup(r.content, "lxml") 

    # Individual products on each page
    product_list = soup.find_all("li", class_="product-grid__item")

    
    # Iterate through product list
    for item in product_list:
        for link in item.find_all("a", href = True): # find href
            print(link["href"])
            product_links.append(baseurl + link["href"]) # add baseurl and individual product links to product_links list

# Empty list for dictionary
whisky_list = []

# Iterate through each product link to find following information below
for link in product_links:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content,"lxml")
    
    # name
    name = soup.find("h1", class_="product-main__name").text.strip()

    # size
    size = soup.find("p", class_="product-main__data").text.strip()[:4]

    # alchol %
    proof = soup.find("p", class_="product-main__data").text.strip()[7:]

    # price
    price = soup.find("p", class_="product-action__price").text.strip()

    # description
    description = soup.find("div", class_="product-main__description").text.strip()

    # in stock status
    in_stock = soup.find("p", class_="product-action__stock-flag").text.strip()

    #country = soup.find("p", class_="product-facts__data").text.strip()

   ###########################################################################################

    # Exception handling
    try:
        # Ratings and reviews
        rating = soup.find("div", class_="review-overview").text.strip()
    except:
        rating = "no rating"
    try:
        # Customer purchase limit
        item_limit = soup.find("p", class_="product-action__message").text.strip()
    except:
        item_limit = "no limit"
    try:
        # Price per litre
        per_litre = soup.find("p", class_="product-action__unit-price").text.strip()
    except:
        per_litre = "n/a"
    try:
        # The type of whisky
        style = soup.find("ul", class_="product-main__meta").text.strip()
    except:
        style = "n/a"
    
    ###############################################################################################

    # Store scraped data to dictionary with keys
    whisky = {
        "name":name,
        "style": style,
        "size": size,
        "alohol_percentage": proof,
        "rating": rating,
        "in_stock": in_stock, 
        "price": price,
        "price_per_litre": per_litre,
        "customer_item_limit": item_limit,
        "description": description,
    }

    whisky_list.append(whisky) # Add dictionary of each scraped product to whisky_list

print(whisky_list)