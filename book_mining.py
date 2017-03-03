from bs4 import BeautifulSoup
import requests
from time import sleep
import re
import sqlite3

#baseurl = "http://shop.oreilly.com/category/browse-subjects/data.do?sortby=publicationDate&page="
#baseurl = "http://shop.oreilly.com/category/browse-subjects/business.do?sortby=publicationDate&page="
#baseurl = "http://shop.oreilly.com/category/browse-subjects/design.do?sortby=publicationDate&page="
#baseurl = "http://shop.oreilly.com/category/browse-subjects/web-development.do?sortby=publicationDate&page="
#baseurl = "http://shop.oreilly.com/category/browse-subjects/microsoft.do?sortby=publicationDate&page="
#baseurl = "http://shop.oreilly.com/category/browse-subjects/programming/python.do?sortby=publicationDate&page="
#baseurl = "http://shop.oreilly.com/category/browse-subjects/programming/java.do?sortby=publicationDate&page="
#baseurl = "http://shop.oreilly.com/category/browse-subjects/programming/javascript.do?sortby=publicationDate&page="
#baseurl = "http://shop.oreilly.com/category/browse-subjects/programming/dotnet.do?sortby=publicationDate&page="
#baseurl = "http://shop.oreilly.com/category/browse-subjects/programming/php.do?sortby=publicationDate&page="
#baseurl = "http://shop.oreilly.com/category/browse-subjects/programming/android-programming.do?sortby=publicationDate&page="
baseurl = "http://shop.oreilly.com/category/browse-subjects/programming/ios-programming.do?sortby=publicationDate&page="
NUM = 0 
NUM_PAGES = 7
books = []
conn = sqlite3.connect('program_book.db')
c = conn.cursor()

def is_video(td):
    """ It's a video if has exactly one pricelabel, and if the stripped text inside that pricelabel start with 'video' """
    pricelabels = td('span', 'pricelabel')
    return (len(pricelabels) == 1 and pricelabels[0].text.strip().startswith("Video"))

def ebook_price(td):
    prices = td('span', 'pricelabel')
    try:
        ebook_prices = prices[0].find('span', 'price')
    except IndexError:
        return '0.00'
    else:
        return ebook_prices.text.split('$')[1] 

def book_info(num, td):
    """Given a BeautifulSoup <td> tag representing a book, extract the book's details and return a dict"""
    title = td.find("div", "thumbheader").a.text
    try:
        author_name = td.find('div', 'AuthorName').text
    except AttributeError:
        author_name = " "
    authors = re.sub("^By ", "", author_name)
    isbn_link = td.find("div", "thumbheader").a.get("href")
    isbn = re.match("/product/(.*)\.do", isbn_link).group(1)
    date = td.find("span", "directorydate").text.strip()
    price = ebook_price(td)
    
    return (num,title,authors,isbn,date,price)
    

for page_num in range(1, NUM_PAGES + 1):
    print "souping page", page_num, ",", "found so far"
    url = baseurl + str(page_num)
    soup = BeautifulSoup(requests.get(url).text, 'html5lib')

    for td in soup('td', 'thumbtext'):
        if not is_video(td):
            NUM += 1
            books.append(book_info(NUM, td))

c.executemany('INSERT INTO ios VALUES(?,?,?,?,?,?)', books)
conn.commit()
conn.close()

#filename = "book_info.txt"
#with open(filename, 'a+') as f:
#    f.write(str(books))


