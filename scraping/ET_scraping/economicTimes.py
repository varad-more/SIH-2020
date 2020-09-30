from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")  #configure webdriver to use Chrome browser, set path

headlines=[] #List to store name of the product
dates=[] #List to store price of the product
descriptions=[] #List to store rating of the product

driver.get("https://economictimes.indiatimes.com/news/company/corporate-trends")

content = driver.page_source
soup = BeautifulSoup(content)
# print(soup)

div = soup.find('div',attrs={'class':'tabdata'})

# print(div)
for a in div.findAll('div', attrs={'class':'eachStory'}):
	#print("loop")
	print(a)
	name=a.find('a', attrs={'itemprop':'url'})
	date = a.find('time')
	description=a.find('p')
	
	try:
		headlines.append(name.text)
		dates.append(date.text)
		descriptions.append(description.text)
	except:
		pass

df = pd.DataFrame({'Product Name':headlines,'Time':dates,'Summary':descriptions}) 
df.to_csv('headlines.csv', index=False, encoding='utf-8')