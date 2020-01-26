import requests
 
file_url="http://www.dtcc.com/~/media/Files/Downloads/WhitePapers/oxera_2004.pdf"


r = requests.get(file_url, stream = True) 
  
with open("/home/suraj/Desktop/web_scraping/Downloaded.pdf","wb") as pdf: 
    for chunk in r.iter_content(chunk_size=1024): 
         # writing one chunk at a time to pdf file 
         if chunk: 
             pdf.write(chunk)