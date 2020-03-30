

from tika import parser
import nltk  
#nltk.download('punkt')
#nltk.download('all')
import requests
#import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.translate.bleu_score import sentence_bleu,corpus_bleu
lemmatizer = WordNetLemmatizer()

 
#file_url="http://www.dtcc.com/~/media/Files/Downloads/WhitePapers/oxera_2004.pdf"
#file_url ="https://www1.nseindia.com/corporate/HINDUNILVR_31122019164401_IntimationofTradingWindowClosedPeriod_577.pdf"
file_url="https://www1.nseindia.com/corporate/HINDUNILVR_17022020190816_PostalBallotNoticeandForm.pdf"


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
subject=""
def find_sub():
    f = open("newfile.txt","r+")
    for line in f.readlines():
        if line[:3]=="Sub":
            #print(line)
            linesub = line[5:]
    print ("\n \n")
    print(linesub)
    subject=linesub

def nltk_check():

# string1 = "A dividend is the distribution of reward from a portion of the company's earnings and is paid to a class of its shareholders. Dividends are decided and managed by the company’s board of directors, though they must be approved by the shareholders through their voting rights. Dividends can be issued as cash payments, as shares of stock, or other property, though cash dividends are the most common. Along with companies, various mutual funds and exchange traded funds (ETF) also pay dividends"
#string1 = "A traditional stock split is also known as a forward stock split. A reverse stock split is the opposite of a forward stock split. A company that issues a reverse stock split decreases the number of its outstanding shares and increases the share price. Like a forward stock split, the market value of the company after a reverse stock split would remain the same. A company that takes this corporate action might do so if its share price had decreased to a level at which it runs the risk of being delisted from an exchange for not meeting the minimum price required to be listed. A company might also reverse split its stock to make it more appealing to investors who may perceive it as more valuable if it had a higher stock price"
    string1="Postal Ballot Notice for  appointment of  Mr.  Wilhelmus Uijen as Whole-time Director of the Company".split()
    #string1
#    print (string1)
    stocksplit = "appointment of CEO, as whole-time."   #"A traditional stock split is also known as a forward stock split. A reverse stock split is the opposite of a forward stock split. A company that issues a reverse stock split decreases the number of its outstanding shares and increases the share price. Like a forward stock split, the market value of the company after a reverse stock split would remain the same. A company that takes this corporate action might do so if its share price had decreased to a level at which it runs the risk of being delisted from an exchange for not meeting the minimum price required to be listed. A company might also reverse split its stock to make it more appealing to investors who may perceive it as more valuable if it had a higher stock price".split()#['stock','split','shares','forward','reverse']
    dividend = "A dividend is the distribution of reward from a portion of the company's earnings and is paid to a class of its shareholders. Dividends are decided and managed by the company’s board of directors, though they must be approved by the shareholders through their voting rights. Dividends can be issued as cash payments, as shares of stock, or other property, though cash dividends are the most common. Along with companies, various mutual funds and exchange traded funds (ETF) also pay dividends".split()#['dividend','bonus','interim','annual','profit','sum']

# PREPROCESSING - CASE FOLDING
    string1 = string1.lower()
# PREPROCESSING - TOKENIZATION
    tokens = nltk.word_tokenize(string1)

    removelist = []

    for i in range(len(tokens)-1):
        if tokens[i] in stopwords.words('english'):
        # print(tokens[i])
            removelist.append(tokens[i])

# print(tokens)

    for i in removelist:
        tokens.remove(i)

# print(tokens)

    removelist = []

    for i in range(len(stocksplit)-1):
        if stocksplit[i] in stopwords.words('english'):
        # print(stocksplit[i])
            removelist.append(stocksplit[i])

# print(tokens)

    for i in removelist:
        stocksplit.remove(i)

# print(tokens)

    removelist = []

    for i in range(len(dividend)-1):
        if dividend[i] in stopwords.words('english'):
        # print(dividend[i])
            removelist.append(dividend[i])

# print(tokens)

    for i in removelist:
        dividend.remove(i)

# print(tokens)

# PREPROCESSING - LEMMATIZATION
    for i in range(len(tokens)-1):
        tokens[i] = lemmatizer.lemmatize(tokens[i])

    for i in range(len(stocksplit)-1):
        stocksplit[i] = lemmatizer.lemmatize(stocksplit[i])

    for i in range(len(dividend)-1):
        dividend[i] = lemmatizer.lemmatize(dividend[i])

# print(tokens)


# PROCESSING - BLEU
# print([stocksplit, dividend])
    dbleu = sentence_bleu([dividend], tokens, weights=(0.5, 0.5))
    spbleu = sentence_bleu([stocksplit], tokens, weights=(0.5, 0.5))
    if spbleu>dbleu:
        print("Stock split")
    else:
        print("Dividend")



if __name__ == "__main__":
    print ("Searching ###########################")
    download_pdf()
    print ("Reading PDF###########################")
    read_pdf()
    print ("Saving into text format###########################")
    read_file()
    print ("Finding subject###########################")
    find_sub()
    print ("NLTK Process")
    nltk_check()



