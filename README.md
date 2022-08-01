# New Arrivals (in each category) Information in a Bookstore Using Webscraping

In my pilot project, I have used webscraping methods in Python to scrape data off a local bookstore's website (https://www.readings.com.pk/). The data that is scraped is basically the details of few books newly arrived in each category at the bookstore. The final data is stored in a CSV file and around 600+ books details are stored in it. It looks something like this:

![Final Screenshot](/csv_screenshot.png)

# Learn

I will be soon uploading a video on youtube

# Install
For this webscrapiing project, I have used three packages. I have used "bs4" to use the BeautifulSoup class which basically is the main tool to scrap data from the website.
Then, the next package that I will be using is "requests". This will allow me to fetch data is html format for the BeautifulSoup to use.
Last but not the least, I will be using "pandas" to collate the fetched datas to a csv folder.

```

from bs4 import BeautifulSoup
import requests
import pandas as pd

```
