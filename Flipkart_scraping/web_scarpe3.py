#download libraries
#download and move chromedriver to the path /usr/lib/chromium-browser/chromedriver

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")  #configure webdriver to use Chrome browser, set path

products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store rating of the product

driver.get("https://www.flipkart.com/laptops/</a>~buyback-guarantee-on-laptops-/pr?sid=6bo%2Cb5g&uniq")
#driver.get("<a href="https://www.flipkart.com/laptops/">https://www.flipkart.com/laptops/</a>~buyback-guarantee-on-laptops-/pr?sid=6bo%2Cb5g&uniq")
#driver.get("<a href="https://www.flipkart.com/laptops/">https://www.flipkart.com/laptops/pr?sid=6bo%2Cb5g&uniq=")

content = driver.page_source
soup = BeautifulSoup(content)
print(soup)

for a in soup.findAll('a',href=True, attrs={'class':'_31qSD5'}):
	print("loop")
	name=a.find('div', attrs={'class':'_3wU53n'})
	price=a.find('div', attrs={'class':'_1vC4OE _2rQ-NK'})
	rating=a.find('div', attrs={'class':'hGSR34'})
	products.append(name.text)
	ratings.append(rating.text) 
	prices.append(price.text)

df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings}) 
df.to_csv('products.csv', index=False, encoding='utf-8')
