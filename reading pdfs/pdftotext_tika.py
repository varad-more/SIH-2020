from tika import parser
import time

def read_pdf():
    raw = parser.from_file('1.pdf')
    print(raw['content'])
    file1 = open("output_pdftotext_tika.txt","w+")
    file1.write(raw['content'])
    file1.close()

def save_file():
    file1 = open("output_pdftotext_tika.txt","r")
    file1.read()
    
if __name__ == "__main__":
	start_time= time.time()
	read_pdf()
	save_file()
	print("time = ", time.time()-start_time)
