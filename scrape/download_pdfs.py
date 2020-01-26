import requests
 
url="https://www.business-standard.com/article/printer-friendly-version?article_id=120012401722_1"
# download the url contents in binary format
myfile = requests.get(url)

open('/home/suraj/Desktop/web_scraping/new.txt', 'wb').write(myfile.content)