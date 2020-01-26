from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
driver =webdriver.Chrome(ChromeDriverManager().install())
products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store rating of the product
url="https://www.moneycontrol.com/stocks/marketinfo/upcoming_actions/home.html"
driver.get(url)

content = driver.page_source
soup = BeautifulSoup(content,"lxml")
print(soup.find('a',attrs={'class':'wrap-inner'}))

for a in soup.findAll('div',href=True, attrs={'class':'main'}): #class="tbldata36 PT10"
    for b in soup.findAll('div',href=True, attrs={'class':'PA10'}):
        for c in soup.findAll('div',href=True, attrs={'class':'FL'}):
            name=a.find('div', attrs={'class':'tbldata36 PT10'})
            print(name)
    
#df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings}) 
#df.to_csv('products.csv', index=False, encoding='utf-8')
