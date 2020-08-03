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
import docx
import mysql.connector
import mysql
import ssl
import requests


def read_pdf(pdf):
    '''Writes and then reads pdf data into txt file'''
    raw = parser.from_file(pdf)
    flag = 1
    # print(raw['content'])
    
    file1 = open("output_of_pdf_read.txt","w")
    
    try:
        file1.write(raw['content'])
        # print(raw['content'])
    except:
        flag = 0
    if flag==1:
        file1.close()
        file2 = open("output_of_pdf_read.txt","r") 
        text_string = file2.read()
    else:
        text_string = ""
        text_string = read_pdf_by_ocr(pdf)
    return text_string


def read_pdf_by_ocr(pdf): 
    '''Writes and then reads image of pdfs' data into txt file'''
    pages = convert_from_path(pdf, 500)
    image_counter = 1
    for page in pages:
        filename = "page_"+str(image_counter)+".jpg"
        page.save(filename, 'JPEG')
        image_counter = image_counter + 1
    filelimit = image_counter-1
    outfile = "pdf_output\\output_of_pdf_read.txt"
    file1 = open(outfile, "a") #check append mode
    for i in range(1, filelimit + 1): 
        filename = "page_"+str(i)+".jpg"
        text = str((pytesseract.image_to_string(Image.open(filename))))
        text = text.replace('-\n', '')
        file1.write(text)
    file1.close()
    file2 = open("pdf_output\\output_of_pdf_read.txt","r") 
    text_file = file2.read()
    return text_file


def write_docx_file(ms_doc):
    doc = docx.Document("ms_doc")
    all_paras = doc.paragraphs
    len(all_paras)
    file1 = open("doc_output\\output_of_docx_read.txt","w")
    for para in all_paras:
        try:
            file1.write(para.text)
        except UnicodeEncodeError:
            pass
    file2 = open("doc_output\\output_of_docx_read.txt","r") 
    text_file = file2.read()
    return text_file


def filter_spans(spans):
    # Spacy fn to filter a sequence of spans so they don't contain overlaps
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
    '''NLP for entity extraction
    Complete usage to be done soon'''
    nlp = spacy.load('en_core_web_lg')
    doc = nlp(text_string) 
    # print("\n*** CURRENCY RELATIONS ***\n")
    relations = extract_currency_relations(doc)
    extracted_entities = [(i.text_string, i.label_) for i in doc.ents]
    print(extracted_entities)


def get_ca_type_1(text_string):  
    '''Regular expressions to extract type of CA'''
    text_string = text_string.lower()
    text_string = text_string.replace('-\n', '')
    word_search = {'type':["other",
                    "dividend", 
                    "bonus", 
                    "stock split", 
                    "reverse stock split", 
                    "rights issue", 
                    "merger and acquisition", 
                    "employee"], 
                    'regex':[r"( bankrupt(cy| ))|( demerge )|( liquidat)",
                     r"(( interim| final|) dividend)|( interim)",
                     r"( bonus (right|issue|share|))",
                     r"(reverse{0} stock split)|( split)",
                     r"( reverse stock split)|(reverse)",
                     r"((issue(. | ))(right(s | )))|(rights (issue|basis|))",
                     r"( merger)|( merge)|( acquisition)|( acquir(.*))",
                     r"(employee)|(scheme)" ] ,
                    'sum':[0, 0, 0, 0, 0, 0, 0, 0]}
    df = pd.DataFrame(word_search)
    num = 0
    for row in df.itertuples():
        regex = row.__getattribute__('regex')
        df['sum'][num] = len(re.findall(regex, text_string))
        num = num + 1
    df2 = ((df.loc[df['sum'] == df['sum'].max()] ))
    if(len(df.index) > 1):
        df2 = df2[:1]
    ca_name = str(df2['type'].to_string(index=False))
    ca_name = ca_name.strip()
    return ca_name


def get_scrip(text_string):
    scrip=""
    text_string = text_string.lower()
    regex = r"((security code)|(scrip code)|(code))(.*)( \d\d\d\d\d\d)"
    # (code.? bse)|(bse code)|
    match = re.search(regex, text_string)  
    if match != None:
        scrip = match.group(6)
    return scrip


def get_date(pdf):
    '''Extraction of announcement date from metadata of file'''
    raw = parser.from_file(pdf)
    md = raw['metadata']
    try:
        date = md['date']
    except KeyError:
        try:
            date = md['Creation-Date']
        except:
            date = '2020-01-01'
    return(date[0:10])


def get_other_dates(pdf,text_string):
    ann_date = get_date(pdf)
    ex_date=""
    rec_date=""
    pay_date=""
    nlp = spacy.load('en_core_web_lg')
    doc = nlp(text_string) 
    extracted_entities = [(i.text, i.label_) for i in doc.ents]
    # print(extracted_entities)
    dates=set()
    dates.add(pd.to_datetime(ann_date).date())
    for i in extracted_entities:
        if (i[1]) == 'DATE':
            if len(i[0])>8:
                try:
                    thisdate = pd.to_datetime(i[0])
                    if(thisdate.year == pd.to_datetime(ann_date).year):
                        dates.add(thisdate)
                except:
                    pass
    dates = sorted(dates)
    datecount = len(dates)
    if (datecount==3):
        ex_date = str(dates[0])
        rec_date = str(dates[1])
        pay_date = str(dates[2])
    if (datecount==2):
        ex_date = str(dates[0])
        rec_date = str(dates[1])
        # pay_date = dates[2]
    return ex_date[0:10],rec_date[0:10],pay_date[0:10]


def get_div_data(text_string):
    pattern = re.compile(r"( z l | Z l | zl | Zl )")
    text_string = pattern.sub(r" rs 1 ", text_string)
    # print(text_string)

    # face value per share extraction
    fv = ""
    regex = r"(\d+)(.*) ((per|every) equity share(.*))(\d+)"
    match = re.search(regex, text_string)  
    if match != None:
        fv = "Rs. "+ match.group(1) +"per equity share of Rs. "+ match.group(6)  #remember to change .group(par) after changing regex
    # percentage extraction
    perc=""
    regex = r"((\d+)\.(\d+)( |)%) | (\d+)( |)%" # considers the first occurence
    match = re.search(regex, text_string)  
    if match != None:
        perc = match.group(0)
    return perc,fv


def get_ss_data(text_string):
    pattern = re.compile(r"( z l | Z l | zl | Zl )") 
    # This fixes a small errror that occurs when rupee symbol is used which misreads 1 as l
    text_string = pattern.sub(r" rs 1 ", text_string)

    # face value per share
    fv = ""
    regex = r"(\d+)(.*) ((per|every) equity share(.*))(\d+)"
    match = re.search(regex, text_string)  
    if match != None:
        fv = "Rs. "+ match.group(1) +"per equity share of Rs. "+ match.group(6)  #remember to change .group(par) after changing regex
    return fv


def connect_database():
    conn = mysql.connector.connect(host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com',
                                        user='admin',
                                        password='SIH_2020',
                                        database='web_server')
    cursor = conn.cursor()
    if conn.is_connected():
        cursor.execute("show tables")
        res = cursor.fetchall()
        print("Available databases: ", res,"\n")

    return(conn,cursor)


def pdf_load(conn,cursor):
    cursor.execute("SELECT url_of_file,company_name FROM dashboard_file_download where ca_extracted=0 limit 100")
    pdf_links_from_table = pd.DataFrame(cursor.fetchall())
    if len(pdf_links_from_table)!=0:
        # print(pdf_links_from_table)
        pdf_links = pdf_links_from_table[0].tolist()
        # company_name = pdf_links[1].tolist()
        # print("company links: ",company_name)
        
        for link in pdf_links:
            # try:
                r = requests.get(link,verify=False,stream=True,timeout=(5,20))
                with open('data.pdf', 'wb') as fd:
                    for chunk in r.iter_content(2000):
                        fd.write(chunk)
                
                print(link)
                text_string = read_pdf("data.pdf")
                
                print("------------------------------")
                # print(text_string)
                # print("------------------------------")
                
                
                sql = "UPDATE dashboard_file_download SET ca_extracted=0 WHERE url_of_file=%s"
                cursor.execute(sql ,(link,))

                scrip_code = get_scrip(text_string)
                date_ca = get_date("data.pdf")
                ca_name = get_ca_type_1(text_string)
                ex_date, rec_date, pay_date = get_other_dates("data.pdf", text_string)
                if scrip_code!="":
                    security_id_type = "scrip code"
                else:
                    security_id_type = "trading symbol"
                print (date_ca ,ca_name, security_id_type,ex_date,rec_date , pay_date )
                
                if ca_name=='dividend':
                    perc, fv = get_div_data(text_string)
                    remarks = fv
                    sql = """INSERT INTO dashboard_dashboard (date_ca , 
                    ca_name, 
                    security_id_type,
                    ex_date,
                    rec_date , 
                    pay_date ,
                    remarks)
                    VALUES
                    (date_ca , 
                    ca_name, 
                    security_id_type,
                    ex_date,
                    rec_date , 
                    pay_date ,
                    remarks) """
                    print (date_ca ,ca_name, security_id_type,ex_date,rec_date , pay_date ,remarks)
                elif ca_name=='stock split':
                    fv = get_ss_data(text_string)
                    remarks = fv
                    sql = """INSERT INTO dashboard_dashboard (date_ca , 
                    ca_name , 
                    security_id_type,
                    ex_date , 
                    rec_date , 
                    pay_date ,
                    remarks )
                    VALUES
                    (date_ca , 
                    ca_name , 
                    security_id_type,
                    ex_date , 
                    rec_date , 
                    pay_date ,
                    remarks ) """
                else:       
                    sql = """INSERT INTO dashboard_dashboard (date_ca , 
                    ca_name , 
                    security_id_type,
                    ex_date , 
                    rec_date , 
                    pay_date ,
                    remarks)
                    VALUES 
                    (date_ca , 
                    ca_name , 
                    security_id_type,
                    ex_date , 
                    rec_date , 
                    pay_date ,
                    remarks) """
                
                cursor.execute(sql)
                
            # except:
            #     # cursor.execute("UPDATE crawler_2 set url_error=1 WHERE url_of_file=%s",(link,))
            #     print("couldn't download from "+link)




if __name__ == "__main__":
    start_time = time.time()
    conn,cursor = connect_database()
    print(conn)

    pdf_load(conn,cursor)
    conn.commit()

    print("main time = ", time.time() - start_time)
        