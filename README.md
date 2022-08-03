# New Arrivals (each category) Information in a Bookstore Using Webscraping

In my pilot project, I have used webscraping methods in Python to scrape data off a local bookstore's website (https://www.readings.com.pk/). The data that is scraped is basically the details of few books newly arrived in each category at the bookstore. The final data is stored in a CSV file and around 600+ books details are stored in it. It looks something like this:



![Final Screenshot](/csv_screenshot.png)


# Learn

I will be soon uploading a video on youtube


# Install
For this webscrapiing project, I have used three packages. 

I have used "bs4" to use the BeautifulSoup class which basically is the main tool to scrap data from the website.

Then, the next package that I will be using is "requests". This will allow me to fetch data is html format for the BeautifulSoup to use.

Last but not the least, I will be using "pandas" to collate the fetched datas to a csv folder.

```

from bs4 import BeautifulSoup
import requests
import pandas as pd

```


# Usage

The website that I used is of a local bookstore in my hometown (Lahore) known as "Readings". The url of the website is kept as a variable that will be used to in "request" module to get the HTML format and later will be used to complete links as well. The website looks like this:


![Homepage Screenshot](/homepage_ss.png)


And what I am looking to target is the categories listed on the left of homepage. I would access each categories and scrap out the new book arrivals of each category. These will be only first few books that will be on the first page of the categories. The variable is given below.

```

READINGS_URL = "https://www.readings.com.pk"

```

Then using request module, the total data on the webpage is fetched as in an html format.

```

homepage = requests.get(READINGS_URL)
homepage_html = homepage.text

```

Then the BeautifulSoup module is initiated on the homepage. This will be used to target the categories that have been listed on the homepage:

```

homepage_soup = BeautifulSoup(homepage_html, 'html.parser')

```

The list of categories (with number of books) were in a "div" tag with the class "categories_listing" and then further down in a "ul" tag and "a" tag as given below:


![List of Categories Screenshot](/categories_list.png)

My main target was to fetch not only category names, but also its links so that they can be later used to fetch the data in each category.

I created an empty list by the name of "categories" and an empty dictionary by the name of "categories_with_link."

Main purpose is the "categories" list should contain the name of categories only. The dictionary would contain the category names and their associated links.


```

div_tag = homepage_soup.find(name="div", class_="categories_listings").find(name="ul").find_all(name="a")
categories = []
categories_with_link = {}

```

For loop is initiated in the div tag. The use of "i,getText()" is to extract the name of categories. Then they are appended in the "categories" list. And using 'f"{READINGS_URL}{i['href']}"', the link is extracted of each category. After that the dictionary is appended with the concerned category and its associated link.

```

for i in div_tag:

    category = i.getText()
    categories.append(category)

    links = f"{READINGS_URL}{i['href']}"
    categories_with_link[category] = links

```

The categories_with_link dictionary would look like this:


```

{'Adult Colouring Books': 'https://www.readings.com.pk/pages/category.aspx?Category=73&Level=Level1&BookType=N', 
'Adult Graphic Novels': 'https://www.readings.com.pk/pages/category.aspx?Category=27&Level=Level1&BookType=N', 
'Anthropology': 'https://www.readings.com.pk/pages/category.aspx?Category=17&Level=Level1&BookType=N', 
'Archaeology': 'https://www.readings.com.pk/pages/category.aspx?Category=19&Level=Level1&BookType=N', 
'Architecture': 'https://www.readings.com.pk/pages/category.aspx?Category=60&Level=Level1&BookType=N', 
'Art': 'https://www.readings.com.pk/pages/category.aspx?Category=56&Level=Level1&BookType=N', 
'Automobiles': 'https://www.readings.com.pk/pages/category.aspx?Category=4&Level=Level1&BookType=N', ...}

```

The categories list would look like this:

```

['Adult Colouring Books', 'Adult Graphic Novels', 'Anthropology', 'Archaeology', 'Architecture', 'Art', 'Automobiles', 'Aviation', 'Biography & Autobiography', 'Body, Mind & Spirit', 'Business', 'Coffee Table', 'Computer', 'Cooking', 'Crafts', 'Education', 'Fashion', 'Fiction', 'Games & Puzzles', 'Gardening & Landscaping', 'Gift Books', 'Guns', 'Health', 'Health & Fitness', 'History', 'Home & Interior', 'Humor', 'Jewelry', 'Journals & Diaries', 'Language', 'Law', 'Linguistics', 'Literary Criticism', 'Literature', 'Mass Communication', 'Medical', 'Middle Eastern Studies', 'Mythology & Folklore', 'Nature', 'New Age/Occult', 'Pakistan Studies', 'Performing Arts', 'Pets', 'Philosophy', 'Photography', 'Politics', 'Psychology', 'Reference', 'Religion', 'Research', 'Science', 'Selfhelp', 'Sociology', 'South Asian Studies', 'Sports', 'Study Guides', 'Travel Guides', 'Travel Writings', 'True Crime', 'Women Studies', 'Writing Skills']

```

A new dictionary is created which will be our final dictionary converted into a CSV file

```
books_dictionary = {"Title": [],
                    "Category": [],
                    "Price": [],
                    "Availability": [],
                    "Links": [],
                    }
```
