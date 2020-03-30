

from tika import parser
import nltk  
# nltk.download('punkt')
import requests
 
#file_url="http://www.dtcc.com/~/media/Files/Downloads/WhitePapers/oxera_2004.pdf"
file_url ="https://www1.nseindia.com/corporate/HINDUNILVR_31122019164401_IntimationofTradingWindowClosedPeriod_577.pdf"



r = requests.get(file_url, stream = True) 
def download_pdf():
    # with open("/home/varad/Downloads/Downloaded.pdf","wb") as pdf: 
    with open("/home/varad/Downloads/Downloaded.pdf","wb") as pdf: 
        for chunk in r.iter_content(chunk_size=1024): 
         # writing one chunk at a time to pdf file 
             if chunk: 
                pdf.write(chunk)
    print ("Downloaded")



def read_pdf():
    raw = parser.from_file('/home/varad/Downloads/Downloaded.pdf')
    #print(raw['content'])
    #print(raw['metadata'])
    file1 = open("myfile.txt","w+")
    file1.write(raw['content'])
    file1.close()

def read_file():
    f = open("myfile.txt","r+")
    newfile = open("newfile.txt","w+")
    #print (f.readline())
    # print (f.readlines())
    
    for line in f.readlines():
        if line == '\n':
            # newfile.write(" ")
            pass

        else:
            newfile.write(line)
        # print("line")
    # print (f.readlines())
        #print (string)
    newfile.close()
    f.close()

def find_sub():
    f = open("newfile.txt","r+")
    for line in f.readlines():
        if line[:3]=="Sub":
            #print(line)
            linesub = line[5:]
    print ("\n \n")
    print(linesub)

    

if __name__ == "__main__":
    print ("Searching ###########################")
    download_pdf()
    print ("Reading PDF###########################")
    read_pdf()
    print ("Saving into text format###########################")
    read_file()
    print ("Finding subject###########################")
    find_sub()
    



