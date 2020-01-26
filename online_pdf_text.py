'''
import PyPDF2
pdf_file = open('example.pdf', 'rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)
number_of_pages = read_pdf.getNumPages()
page = read_pdf.getPage(0)
page_content = page.extractText()
print (page_content.encode('utf-8'))

'''

from tika import parser
import nltk  
# nltk.download('punkt')
import requests
 
#file_url="http://www.dtcc.com/~/media/Files/Downloads/WhitePapers/oxera_2004.pdf"
file_url ="https://www1.nseindia.com/corporate/HINDUNILVR_31122019164401_IntimationofTradingWindowClosedPeriod_577.pdf"



r = requests.get(file_url, stream = True) 
def download_pdf():
    with open("/home/varad/Downloads/Downloaded.pdf","wb") as pdf: 
        for chunk in r.iter_content(chunk_size=1024): 
         # writing one chunk at a time to pdf file 
             if chunk: 
                pdf.write(chunk)
    print ("Downloaded")





def read_pdf():
    raw = parser.from_file('/home/varad/Downloads/Downloaded.pdf')
    print(raw['content'])
    #print(raw['metadata'])
    file1 = open("myfile.txt","w+")
    #file1.write(raw['content'])
    file1.close()

def read_file():
    f = open("myfile.txt","r")
    #print (f.readline())
    print (f.read())
    '''
    for line in f:
        string = f.read()
        print (string)
    '''
    f.close()
    '''
    string.split('\n')
    print (string)
    #' '.join(string.split())
    #print (string)
    #tokens = nltk.word_tokenize(string)
    #print (tokens)
   # f.close()

    #for line in f:
     #   for word in line.split():
      #     print(word)  
    #file1.readlines(100)
    '''
if __name__ == "__main__":
    print ("Searching")
    download_pdf()
    print ("Reading PDF")
    read_pdf()
    print ("Saving into text format")
    read_file()




