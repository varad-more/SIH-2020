
#Python program to scrape website  
#and save quotes from website 
import requests 
from bs4 import BeautifulSoup 
import csv 
  
URL = "http://www.values.com/inspirational-quotes"
r = requests.get(URL) 
  
soup = BeautifulSoup(r.content, 'html5lib') 
#print(soup)
#quotes=[]  # a list to store quotes 

table = soup.find('div', attrs = {'class':'container'}) 

#print(table)

for row in table.findAll('div', attrs = {'class':'all_quotes'}): 
    quote = {} 
    quote['theme'] = row.h5.text 
    quote['url'] = row.a['href'] 
    quote['img'] = row.img['src'] 
    quote['lines'] = row.h6.text 
    quote['author'] = row.p.text 
    quotes.append(quote) 

    print(quote)
