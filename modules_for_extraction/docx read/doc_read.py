import docx
'''
pip install docx
pip install python-docx
'''
doc = docx.Document("a\\ca_reliance.docx")

all_paras = doc.paragraphs
len(all_paras)

file1 = open("a\\output_of_docx_read.txt","w")

for para in all_paras:
    try:
        file1.write(para.text)
    except UnicodeEncodeError:
        file1.write(para.text.replace('\u20b9', 'Rs.'))
print("done")