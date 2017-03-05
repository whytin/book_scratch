#Finding the most popular category of books in O'Reilly
##Overview
Refer to *"Data Science From Scratch"*,  I want to explore which category of books is the largest quantity, and I will recommend you to start studying which kind of books when you are still confused with your future.

![programming_book.png](http://upload-images.jianshu.io/upload_images/5027777-f4ccf1f10ac838fb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![book.png](http://upload-images.jianshu.io/upload_images/5027777-f331001c8f6980a9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

You can fork the project by Github:
**Github:** *http://github.com/whytin/book_scratch*

##Preparation
###Tool
+ **BeautifulSoup4**(a python library designed for dissecting a doucument into a parse tree, we can extract what we need esaily);
Refer to : *http://www.crummy.com/software/BeautifulSoup/*
+ **htmll5lib**(a popular Python parser to handle the HTML format);
+  **requests**(make a HTTP request)

###Environment
+ Linux Mint 18.1 (Unlimited)
+ Python 2.7
+ Sqlite3

###Foundation
* Python
* HTML
* Matplotlib
* SQL

##Start
###Scratch admited
Before you start the project, make sure your target is open to scratch.
Like O'Reilly: *[http://oreilly.com/terms/](http://oreilly.com/terms/)*
Glance over the page I have not found some issues with banning the scratch.
Then we look over the robots.txt file. *[http://shop.oreilly.com/robots.txt](http://shop.oreilly.com/robots.txt)*
We found that :
```
Crawl-delay: 30
Request-rate: 1/30
```
It means that we should delay 30s between two requests.
###Parsing the page
If you know well with HTML, it is easy for you to find out the tags.
**First**, you can select category of data through *[Browse Subjects](http://shop.oreilly.com/category/browse-subjects/data.do)*

**Second**, use the developer tools.
![Paste_Image.png](http://upload-images.jianshu.io/upload_images/5027777-e1943a4936451607.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

It is wise to use the button of **Select an element in the page to inspect it** ,and then find out the tag <td class="thumbtext">
We can extract the title, authors, date, isbn, price of the book.
**Do yourself , you will fall in curiousity.**

###Coding
```
from bs4 import BeautifulSoup
import requests
```
```
#Making a request of url and send to BeautifulSoup parsing with html5lib.
url = "http://shop.oreilly.com/category/browse-subjects/data.do?sortby=publicationDate&page=1"
soup = BeautifulSoup(requests.get(url).text, 'html5lib')
tds = soup('td', 'thumbtext')
```

We found book's title involved the a tag of <div class="thumbheader">, and extract it.
```
titles = [td.find("div", "thumbheader").a.text for td in tds]
``` 
And we can build the function of book_info()
```
#In order to extract the book information like title, authors, isbn, date, price. Return a dict.
def book_info(td):
    title = td.find("div", "thumbheader").a.text
    authors = td.find('div', 'AuthorName').text
    isbn_link = td.find("div", "thumbheader").a.get("href")
    isbn = re.match("/product/(.*)\.do", isbn_link).group(1)
    date = td.find("span", "directorydate").text.strip()
    price = td('span', 'pricelabel')[0].find('span', 'price')
    
    return {
            "tilte": title,
            "authors": authors,
             "isbn": isbn,
             "date":date,
             "price":price  }
```
Scratching:
```
from bs4 import BeautifulSoup
import requests
import re
from time import sleep
base_url = "http://shop.oreilly.com/category/browse-subjects/data.do?sortby=publicationDate&page="
books=[]
NUM_PAGES = 44

for page_num in range(1, NUM_PAGES + 1):
    url = baseurl + str(page_num)
    soup = BeautifulSoup(requests.get(url).text, 'html5lib')
    for td in soup('td', 'thumbtext'):
        books.append(book_info(td))
    sleep(30)
```
Visualization:
```
import matplotlib as plt
def get_year(book):
    return int(book["date"].split()[1])

#Counter(): dict subclass for counting hashable objects
years_counts = Counter(get_year(book) for book in books if get_year(book) <= 2016)
years = sorted(years_counts)
book_counts = [year_counts[year] for year in years]
plt.plot(years, book_counts)
plt.show()
```

##Summary
It is the brief induction of usage of python scratching, using BeautifulSoup and Matplotlib. You can also scratching Amazon website or whatever you want to obtain. Remember you are risk in data scratching, square up your behavior in Internet.
