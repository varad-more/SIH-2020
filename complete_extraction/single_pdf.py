import datefinder
import spacy
from tika import parser
import time
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import glob, io, os
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os
import pandas as pd
import re

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def pdf_to_text(path):
        pagenums = set()
        output = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)
        infile = open(path, 'rb')
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
        infile.close()
        converter.close()
        text = output.getvalue()
        output.close

        return text

def read_pdf(pdf):
    raw = parser.from_file(pdf)
    # print(raw['content'])
    file1 = open("C:\\Temporary\\current\\output_of_pdf_read_1.txt","w")
    try:
        file1.write(raw['content'])
    except:
        print(" --- image pdf problem --- ")
        # read_pdf_by_ocr(pdf)
    file1.close()

def read_pdf_by_ocr(pdf): #check append mode
    pages = convert_from_path(pdf, 500)
    image_counter = 1
    for page in pages:
        filename = "page_"+str(image_counter)+".jpg"
        page.save(filename, 'JPEG')
        image_counter = image_counter + 1
    filelimit = image_counter-1
    outfile = "output_of_pdf_read.txt"
    file2 = open(outfile, "a") 
    for i in range(1, filelimit + 1): 
        filename = "page_"+str(i)+".jpg"
        text = str(((pytesseract.image_to_string(Image.open(filename)))))
        text = text.replace('-\n', '')
        file2.write(text)
    file2.close()

def read_text_file():
    file1 = open("C:\\Temporary\\current\\output_of_pdf_read_1.txt","r")
    text_file = file1.read()
    return text_file

def filter_spans(spans):
    # Spacy function to filter a sequence of spans so they don't contain overlaps
    get_sort_key = lambda span: (span.end - span.start, -span.start)
    sorted_spans = sorted(spans, key=get_sort_key, reverse=True)
    result = []
    seen_tokens = set()
    for span in sorted_spans:
        # Check for end - 1 here because boundaries are inclusive
        if span.start not in seen_tokens and span.end - 1 not in seen_tokens:
            result.append(span)
        seen_tokens.update(range(span.start, span.end))
    result = sorted(result, key=lambda span: span.start)
    return result

def extract_currency_relations(doc):
    # Merge entities and noun chunks into one token
    spans = list(doc.ents) + list(doc.noun_chunks)
    spans = filter_spans(spans)
    with doc.retokenize() as retokenizer:
        for span in spans:
            retokenizer.merge(span)
    relations = []
    for money in doc:
        if money.dep_ in ("attr", "dobj"):
            subject = [w for w in money.head.lefts if w.dep_ == "nsubj"]
            if subject:
                subject = subject[0]
                relations.append((subject, money))
        elif money.dep_ == "pobj" and money.head.dep_ == "prep":
            relations.append((money.head.head, money))
    return relations

def currencies():
    nlp = spacy.load('en_core_web_lg')
    doc = nlp(text_string)
    print("\n*** CURRENCY RELATIONS ***\n")
    relations = extract_currency_relations(doc)
    for r1, r2 in relations:
        print("{:<10}\t{}\t{}".format(r1.text, r2.ent_type_, r2.text))

def get_ca_type_2(text_string):
    text_string = text_string.lower()
    print(text_string)
    '''
    div = {"dividend" : 0, 'interim' : 0}
    bon = {"bonus" : 0, "bonus rights" : 0,"bonus shares" : 0, "bonus issue":0}
    ss = {"stock split": 0, "split":0}
    rss = {"reverse stock split":0, "reverse":0}
    rts = {"rights issue":0, "issue right":0 }
    mrgac = {"merger": 0, "mrgr":0, "acquir":0, "acquisition":0}
    emp = {"employee":0, "scheme":0}
    '''
    oth = {"bankruptcy":0, "demerge":0, "liquidat":0}
    div = {"dividend" : 0, 'interim' : 0}
    bon = {"bonus" : 0 }
    ss = {"stock split": 0, "split ":0}
    rss = {"reverse stock split":0, "reverse":0}
    rts = {"rights issue":0, "issue right":0, "rights":0 }
    mrgac = {"merger": 0, "mrgr":0, "acquir":0, "acquisition":0}
    emp = {"employee":0, "scheme":0}

    ca_dict = {"other":oth, "dividend": div, "bonus": bon, "stock split": ss, "reverse stock split": rss, "rights issue": rts, "merge and acquisition": mrgac, "employee": emp}
    ca_weight = {"other":0, "dividend": 0, "bonus": 0, "stock split": 0, "reverse stock split": 0, "rights issue": 0, "merge and acquisition": 0,"employee": 0}

    print("\n\n", ca_dict)
    for word, ca in ca_dict.items():
        for key in ca:
            ca[key] = text_string.count(word)
    for ca1 in ca_weight:
        values = ca_dict[ca1].values()
        ca_weight[ca1] = sum(values)
    print("\n\n", ca_dict)
    print("\n\n", ca_weight)
    return (str(max(ca_weight, key=ca_weight.get)))

def get_ca_type_1(text_string):   
    text_string = text_string.lower()
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(text_string.lower())
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    filtered_sentence = [] 
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w) 
    # print(word_tokens) 
    # print("\n\n\nfilter ", filtered_sentence)
    print(sum('acquisition' in s for s in filtered_sentence))

    # div = len(re.findall('DEVOPAM', text_string))
    
    # m = re.search('employee', text_string, re.MULTILINE)  # Match
    # <re.Match object; span=(4, 5), match='X'>
    # print(m)
    # print("calc time = ", time.time()-start_time)
    return 'yes'

def get_ca_type_3(text_string):  
    text_string = text_string.lower()
    # regex = r"( bankrupt(cy| ))|( demerge )|( liquidat)"
    # regex = r"(dividend)|(interim)"
    # regex = r"(bonus (right|issue|share|))"
    # regex = r"(reverse{0} stock split)|( split)"
    # regex = r"(reverse stock split)|(reverse)"
    # regex = r"(issue(. | ))(right(s | )|(right(s | )(issue|))"
    # regex = r"(merger)|(mrgr)|(acquisition)|(acquir..)"
    # regex = r"(employee)|(scheme)"
    word_search = {'type':["other",
                    "dividend", 
                    "bonus", 
                    "stock split", 
                    "reverse stock split", 
                    "rights issue", 
                    "merge and acquisition", 
                    "employee"], 
                    'regex':[r"( bankrupt(cy| ))|( demerge )|( liquidat)",
                     r"(dividend)|(interim)",
                     r"(bonus (right|issue|share|))",
                     r"(reverse{0} stock split)|( split)",
                     r"(reverse stock split)|(reverse)",
                     r"((issue(. | ))(right(s | )))|(rights (issue|basis|))",
                     r"(merger)|(mrgr)|(acquisition)|(acquir..)",
                     r"(employee)|(scheme)" ] ,
                    'sum':[0, 0, 0, 0, 0, 0, 0, 0]}
    df = pd.DataFrame(word_search)
    num = 0
    for row in df.itertuples():
        regex = row.__getattribute__('regex')
        df['sum'][num] = len(re.findall(regex, text_string))
        num = num + 1
    df2 = ((df.loc[df['sum'] == df['sum'].max()] ))
    ca_name = str(df2['type'].to_string(index=False))
    ca_name = ca_name.strip()
    return ca_name

def get_date(pdf):
    raw = parser.from_file(pdf)
    md = raw['metadata']
    # print(md)
    try:
        date = md['date']
    except KeyError:
        date = md['Creation-Date']
    return(date[0:10])

def get_other_dates():
    matches = []
    try:
        matches = list(datefinder.find_dates(text_string, index=True, strict=False))
        print(matches)
        for match in matches:
            print("match ",match)
    except TypeError:
        print ("TypeError")
    except Error as e:
        print("An error occured", e)
    finally:
        sorted_dates = sorted(matches)
        print(sorted_dates) 
    rec_date = str(sorted_dates[0])
    pay_date = str(sorted_dates[len(sorted_dates)-1])
    return rec_date, pay_date

def get_div_data(text_string):
    # face value per share
    fv = ""
    regex = r"(\d+)(.*) ((per|equity) equity share(.*))(\d+)"
    match = re.search(regex, text_string)  
    if match != None:
        fv = "Rs. "+ match.group(1) +"per equity share of Rs. "+ match.group(6)  #remember to change .group(par) after changing regex
    perc=""
    regex = r"(\d+).(\d+)% | (\d+)%" # considers the first occurence
    match = re.search(regex, text_string)  
    if match != None:
        print ("match  ", match.group(0))
        perc = match.group(0)
    return perc,fv



if __name__ == "__main__":
    start_time= time.time()
    
    pdf_list = glob.glob("C:\\Temporary\\docs\\corporate_actions\\TCS_2_SELetter.pdf")
    for pdf in pdf_list:
        read_pdf(pdf)
        # text_string = pdf_to_text(pdf)
        # print(text_string)
        text_string = read_text_file()

        date = get_date(pdf)
        # rec_date, pay_date = get_other_dates()
        ca_name = get_ca_type_3(text_string)
        
        if ca_name=='dividend':
            perc,fv = get_div_data(text_string)
            
        elif ca_name=='bonus':
            # ratio = get_bon_data(text_string)
           
        elif ca_name=='stock split':
            # fv,qty = get_ss_data(text_string)

        elif ca_name=='rights issue':
        # print("row x:",date, "\t", ca_name,"\t", pdf)


    print("time = ", time.time()-start_time)
    