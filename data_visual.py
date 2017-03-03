import matplotlib.pyplot as plt
from collections import Counter
import sqlite3
import re

conn = sqlite3.connect('book.db')
c = conn.cursor()

def get_year(book):
    return int(re.findall('[0-9]{4}',str(book))[0])
def sort_counts(year_counts):
    years = sorted(year_counts)
    return [year_counts[year] for year in years]

year_counts1 = Counter(get_year(book) for book in c.execute('SELECT date from data')  if get_year(book)<= 2016)
year_counts2 = Counter(get_year(book) for book in c.execute('SELECT date from business')  if get_year(book)<= 2016)
year_counts3 = Counter(get_year(book) for book in c.execute('SELECT date from design')  if get_year(book)<= 2016)
year_counts4 = Counter(get_year(book) for book in c.execute('SELECT date from web')  if get_year(book)<= 2016)
year_counts5 = Counter(get_year(book) for book in c.execute('SELECT date from microsoft')  if get_year(book)<= 2016)

years1 = sorted(year_counts1)
years2 = sorted(year_counts2)
years3 = sorted(year_counts3)
years4 = sorted(year_counts4)
years5 = sorted(year_counts5)
plt.plot(years1, sort_counts(year_counts1), color='red', marker='o', linestyle='solid', label='data')
plt.plot(years2, sort_counts(year_counts2), color='green', marker='o', linestyle='solid', label='business')
plt.plot(years3, sort_counts(year_counts3), color='blue', marker='o', linestyle='solid', label='design')
plt.plot(years4, sort_counts(year_counts4), color='black', marker='o', linestyle='solid', label='web')
plt.plot(years5, sort_counts(year_counts5), color='yellow', marker='o', linestyle='solid', label='microsoft')

plt.legend(loc=9)
plt.title("Huge changes of various books in O'Reilly")
plt.xlabel("Years")
plt.ylabel("Counts")
plt.show()


