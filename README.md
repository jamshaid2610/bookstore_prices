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

Printing variable to check at the end of the next for loop that the codes are being executed and all the categories and their books have been inserted in the dictionary. 
Then a for loop is executed which takes the url of a category, uses request module to get the concerned html format to be used for BeautifulSoup

```
printing = 0
for category in categories_with_link:

    category_url = categories_with_link[category]
    category_website = requests.get(category_url)
    category_html = category_website.text

    category_soup = BeautifulSoup(category_html, 'html.parser')
    
```
Two tags are being targeted on the category website. Both of them are "div" tags. The "title_div_tag" is for targeting the title of the book and the link as well.
"avail_tag" is used to target other details of the book, later from this tag we will extract the "Availability" and "Price" information of the book.

```
title_div_tag = category_soup.find_all(name="div", class_="product_detail_page_left_colum_author_name")
avail_tag = category_soup.find_all(name="div", class_="new_change_title_plus_cart_button_bottom_area_left")
    
```

A for loop is executed on the "title_div_tag", after which we will target the anchor tag which contains the title of the book. Using getText() we will extract the title name from the anchor tag. The title name extracted were all in lowercase, hence the use of title(). Then the title name is appended to they key "Title" in books_dictionary. We will take this opportunity to add the associated category in books_dictionary using "books_dictionary["Category"].append(category)" The final thing in this for loop is to take out the link associated with the book. To do that we used "anchor_tag['href']" and to complete the link we added 'f"{READINGS_URL}{link}"' as the variable link only gave partial link. Then we appended the links to the key "Links" in books_dictionary. The for loop lasted till all the books and its information listed on the page were appended in the books_dictionary.

```

for title in title_div_tag:
    anchor_tag = title.find_next(name="a")
    title_name = anchor_tag.getText().title()
    books_dictionary["Title"].append(title_name)
    books_dictionary["Category"].append(category)

    link = anchor_tag['href']
    complete_link = f"{READINGS_URL}{link}"
    books_dictionary["Links"].append(complete_link)
    
```

Then a for loop is executed on the "avail_tag". The next "div" tag in "avail_tag" gives the user the status of book's availability, which would be extracted using getText() and then appended in the books_dictionary for the "Availability" key.
To find the price, 'price = a.find_next(name="div", class_="our_price")' is executed. This tag has several prices listed in it hence after getTexT(), we split these items in a list and the last element in the list is the actual price that the bookstore is selling for. Then we append it in books_dictionary for the "Price" key.

```
for a in avail_tag:
    avail = a.find_next(name="div")
    status = avail.getText()
    books_dictionary["Availability"].append(status)

    price = a.find_next(name="div", class_="our_price")
    actual_price = price.getText().split()[-1]
    books_dictionary["Price"].append(actual_price)
```

The final dictionary would look something like this:

```
{'Title': ['Mythic World',
           "Mythographic Color And Discover: Wild Winter: An Artist'S Coloring Book Of Snowy Animals And Hidden Objects",
           '30 Days Of Creativity: Draw, Colour And Discover Your Creative Self',
           'Worlds Of Wonder: A Colouring Book For The Curious', "Fragile World: Color Nature'S Wonders",
           'Johanna Basford Land, Sea, And Sky: Three Colorable Notebooks',
           'How To Draw Inky Wonderlands: Create And Colour Your Own Magical Adventure',
           'The Little Book Of Colour:How To Use The Psychology Of Colour To Transform Your Life',
           'Geomorphia:An Extreme Coloring And Search Challenge',
           'World Of Flowers: A Colouring Book And Floral Adventure'],
 'Category': ['Adult Colouring Books', 'Adult Colouring Books', 'Adult Colouring Books', 'Adult Colouring Books',
              'Adult Colouring Books', 'Adult Colouring Books', 'Adult Colouring Books', 'Adult Colouring Books',
              'Adult Colouring Books', 'Adult Colouring Books'],
 'Price': ['Rs.1841', 'Rs.1795', 'Rs.1615', 'Rs.2065', 'Rs.1435', 'Rs.1165', 'Rs.1525', 'Rs.1211', 'Rs.1075',
           'Rs.2065'], 'Availability': ['Available', 'Out of StockAvailability in 6-8 weeks on receipt of order',
                                        'Out of StockAvailability in 6-8 weeks on receipt of order',
                                        'Out of StockAvailability in 6-8 weeks on receipt of order',
                                        'Out of StockAvailability in 6-8 weeks on receipt of order',
                                        'Out of StockAvailability in 6-8 weeks on receipt of order',
                                        'Out of StockAvailability in 6-8 weeks on receipt of order',
                                        'Out of StockAvailability in 6-8 weeks on receipt of order',
                                        'Out of StockAvailability in 6-8 weeks on receipt of order',
                                        'Out of StockAvailability in 6-8 weeks on receipt of order'],
 'Links': ['https://www.readings.com.pk/pages/BookDetails.aspx?BookID=1371242',
           'https://www.readings.com.pk/pages/BookDetails.aspx?BookID=1367607',
           'https://www.readings.com.pk/pages/BookDetails.aspx?BookID=1358155',
           'https://www.readings.com.pk/pages/BookDetails.aspx?BookID=1294419',
           'https://www.readings.com.pk/pages/BookDetails.aspx?BookID=1294379',
           'https://www.readings.com.pk/pages/BookDetails.aspx?BookID=1364490',
           'https://www.readings.com.pk/pages/BookDetails.aspx?BookID=1345015',
           'https://www.readings.com.pk/pages/BookDetails.aspx?BookID=1195144',
           'https://www.readings.com.pk/pages/BookDetails.aspx?BookID=1158619',
           'https://www.readings.com.pk/pages/BookDetails.aspx?BookID=1171803']}
           
 ```

After the main for loop has been executed, we will have a complete dictionary of all the categories and its first few newest arrivals. Then using pandas module, we will convert the dictionary into a dataframe and then the dataframe will be converted into a CSV file known as "Books Details (Readings)". Index will be kept false and there will be no change to headers as we will be using keys in books_dictionary as headers.


```
df = pd.DataFrame.from_dict(books_dictionary)
df.to_csv("Book Details (Readings).csv", index=False)

```

And as shown above, the final file will look something like this:


![Final Screenshot](/csv_screenshot.png)

You can use the file to filter your favourite category:

![Category Filter](/category_filter.png)

or the price range you are looking for:

![Price Filter](/price_filter.png)

or if the books that are available:

![Availability Filter](/availability_filter.png)

# End Result

This particular project gave us information for about more than 600 books in matter of minutes. 

# Feedback

Given that this is my first personal project, please do send me a feedback at jamshaid2610@gmail.com :smile:
