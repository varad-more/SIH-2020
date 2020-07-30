
from fpdf import FPDF 
import cv2 as cv
import time

start = time.time()
# save FPDF() class into a  
# variable pdf 
pdf = FPDF() 
  
# Add a page 
pdf.add_page() 
  
# set style and size of font  
# that you want in the pdf 
pdf.set_font("Times", 'B',size = 15) 
  
# create a cell 
pdf.cell(200, 10, txt = "Corporate Actions",  
         ln = 1, align = 'C', ) 

pdf.set_font("Times", size = 14) 

# add another cell 
pdf.cell(200, 10, txt = "This is a document generated by team Pythanos for FIS Global \n", 
         ln = 2, align = 'C') 
  
nm = 'NSE'

pdf.set_font("Times", size = 12) 
pdf.cell(200, 10, txt = "Company Name:" +nm, 
         ln = 2, align = 'L') 


#Image insertion
import matplotlib.pyplot as plt

data = {'apple': 10, 'orange': 15, 'lemon': 5, 'lime': 20}
names = list(data.keys())
values = list(data.values())

fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
axs[0].bar(names, values)
axs[1].scatter(names, values)
axs[2].plot(names, values)
fig.suptitle('Categorical Plotting')
plt.savefig('1.png')

pdf.image('1.png', x = None, y = None) #w = 64, h = 64, type = '', link = '')

# save the pdf with name .pdf 
pdf.output("Company"+nm+".pdf")    
print (time.time()-start)