from bs4 import BeautifulSoup
import pandas as pd
import requests


READINGS_URL = "https://www.readings.com.pk"

homepage = requests.get(READINGS_URL)
homepage_html = homepage.text

homepage_soup = BeautifulSoup(homepage_html, 'html.parser')

div_tag = homepage_soup.find(name="div", class_="categories_listings").find(name="ul").find_all(name="a")

categories = []
categories_with_link = {}

for i in div_tag:
    category = i.getText()
    categories.append(category)

    links = f"{READINGS_URL}{i['href']}"
    categories_with_link[category] = links


books_dictionary = {"Title": [],
                    "Category": [],
                    "Price": [],
                    "Availability": [],
                    "Links": [],
                    }

printing = 0
for category in categories_with_link:

    category_url = categories_with_link[category]
    category_website = requests.get(category_url)
    category_html = category_website.text

    category_soup = BeautifulSoup(category_html, 'html.parser')

    title_div_tag = category_soup.find_all(name="div", class_="product_detail_page_left_colum_author_name")
    avail_tag = category_soup.find_all(name="div", class_="new_change_title_plus_cart_button_bottom_area_left")

    for title in title_div_tag:
        anchor_tag = title.find_next(name="a")
        title_name = anchor_tag.getText().title()
        books_dictionary["Title"].append(title_name)
        books_dictionary["Category"].append(category)

        link = anchor_tag['href']
        complete_link = f"{READINGS_URL}{link}"
        books_dictionary["Links"].append(complete_link)

    for a in avail_tag:
        avail = a.find_next(name="div")
        status = avail.getText()
        books_dictionary["Availability"].append(status)

        price = a.find_next(name="div", class_="our_price")
        actual_price = price.getText().split()[-1]
        books_dictionary["Price"].append(actual_price)

    printing += 1
    print(f"Printing {printing} out of {len(categories)} categories")
    category_website.close()

df = pd.DataFrame.from_dict(books_dictionary)
df.to_csv("Book Details (Readings).csv", index=False)


