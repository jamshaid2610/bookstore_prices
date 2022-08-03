from bs4 import BeautifulSoup
import pandas as pd
import requests


"""The website that I will be using is a local bookstore in my hometown (Lahore) known as Readings. The url of the website
is kept as a variable to be used."""

READINGS_URL = "https://www.readings.com.pk"

"""Then using request module, the total data on the webpage is fetched as in an html format."""

homepage = requests.get(READINGS_URL)
homepage_html = homepage.text


"""Initiation of BeautifulSoup on the homepage. This will be used to target the categories that have been listed on the
homepage"""

homepage_soup = BeautifulSoup(homepage_html, 'html.parser')

"""The list of categories (with number of books) were in a "div" tag with the class "categories_listing". My main target
was to fetch not only category names, but also its links so that they can be later used to fetch the data in each category.
I created an empty list by the name of "categories" and an empty dictionary by the name of "categories_with_link."
 Main purpose is the "categories" list should contain the name of categories only. The dictionary would contain the category
 names and their associated links."""

div_tag = homepage_soup.find(name="div", class_="categories_listings").find(name="ul").find_all(name="a")

categories = []
categories_with_link = {}


"""For loop is initiated in the div tag. The use of "i,getText()" is to extract the name of categories. Then they are appended
in the "categories" list. And using 'f"{READINGS_URL}{i['href']}"', the link is extracted of each category. After that the
dictionary is appended with the concerned category and its associated link."""

for i in div_tag:

    category = i.getText()
    categories.append(category)

    links = f"{READINGS_URL}{i['href']}"
    categories_with_link[category] = links

"""A new dictionary is created which will be our final dictionary converted into a CSV file"""

books_dictionary = {"Title": [],
                    "Category": [],
                    "Price": [],
                    "Availability": [],
                    "Links": [],
                    }

"""Printing variable to check at the end of the next for loop that the codes are being executed and all the categories and
their books have been inserted in the dictionary. Then a for loop is executed which takes the url of a category, uses request
module to get the concerned html format to be used for BeautifulSoup"""

printing = 0
for category in categories_with_link:

    category_url = categories_with_link[category]
    category_website = requests.get(category_url)
    category_html = category_website.text

    category_soup = BeautifulSoup(category_html, 'html.parser')

    """Two tags are being targeted. Both of them are "div" tags. The "title_div_tag" is for targeting the title of the book
    and the link as well.
    "avail_tag" is used to target other details of the book, later from this tag we will extract the "Availability" and "Price"
    information of the book"""

    title_div_tag = category_soup.find_all(name="div", class_="product_detail_page_left_colum_author_name")
    avail_tag = category_soup.find_all(name="div", class_="new_change_title_plus_cart_button_bottom_area_left")

    """A for loop is executed on the "title_div_tag", after which we will target the anchor tag which contains the title
    of the book. Using getText() we will extract the title name from the anchor tag. The title name extracted were all in
    lowercase, hence the use of title(). Then the title name is appended to they key "Title" in books_dictionary. We will
    take this opportunity to add the associated category in books_dictionary using "books_dictionary["Category"].append(category)"
    The final thing in this for loop is to take out the link associated with the book. To do that we used "anchor_tag['href']"
    and to complete the link we added 'f"{READINGS_URL}{link}"' as the variable link only gave partial link. Then we appended
    the links to the key "Links" in books_dictionary. The for loop lasted till all the books and its information
    listed on the page were appended in the books_dictionary."""

    for title in title_div_tag:
        anchor_tag = title.find_next(name="a")
        title_name = anchor_tag.getText().title()
        books_dictionary["Title"].append(title_name)
        books_dictionary["Category"].append(category)

        link = anchor_tag['href']
        complete_link = f"{READINGS_URL}{link}"
        books_dictionary["Links"].append(complete_link)

    """Then a for loop is executed on the "avail_tag". The next "div" tag in "avail_tag" gives the user the status of
    book's availability, which would be extracted using getText() and then appended in the books_dictionary for the "Availability"
    key.
    To find the price, 'price = a.find_next(name="div", class_="our_price")' is executed. This tag has several prices listed in it
    hence after getTexT(), we split these items in a list and the last element in the list is the actual price that the
    bookstore is selling for. Then we append it in books_dictionary for the "Price" key. """

    for a in avail_tag:
        avail = a.find_next(name="div")
        status = avail.getText()
        books_dictionary["Availability"].append(status)

        price = a.find_next(name="div", class_="our_price")
        actual_price = price.getText().split()[-1]
        books_dictionary["Price"].append(actual_price)

    printing += 1
    print(f"Printing {printing} out of {len(categories)} categories")
    print(books_dictionary)

"""After the main for loop has been executed, we will have a complete dictionary of all the categories and its first few
newest arrivals. Then using pandas module, we will convert the dictionary into a dataframe and then the dataframe will be
converted into a CSV file known as "Books Details (Readings)". Index will be kept false and there will be no change to headers
 as we will be using keys in books_dictionary as headers."""


df = pd.DataFrame.from_dict(books_dictionary)
df.to_csv("Book Details (Readings).csv", index=False)

















