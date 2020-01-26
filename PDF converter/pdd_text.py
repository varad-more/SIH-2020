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



def read_pdf():
    raw = parser.from_file('example1.pdf')
    print(raw['content'])
    #print(raw['metadata'])
    file1 = open("myfile.txt","w+")
    file1.write(raw['content'])
    file1.close()

def save_file():
    file1 = open("myfile.txt","r")
    file1.read()
    
#if main = _init_
read_pdf()
save_file()