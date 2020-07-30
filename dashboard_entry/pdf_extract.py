import datefinder
import spacy
from tika import parser
import time
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import mysql.connector
from mysql.connector import Error
import glob, io, os

def read_pdf(pdf):
    raw = parser.from_file(pdf)
    # print(raw['content'])
    # print("\nMETADATA\n\n", raw['metadata'])
    file1 = open("output_of_pdf_read.txt","w+")
    file1.write(raw['content'])
    file1.close()

def read_text_file():
    file1 = open("output_of_pdf_read.txt","r")
    text_file = file1.read()
    return text_file

def filter_spans(spans):
    # Filter a sequence of spans so they don't contain overlaps
    # For spaCy 2.1.4+: this function is available as spacy.util.filter_spans()
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

def get_ca_type(text_string):  
    text_string = text_string.lower()
    '''
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(text_string.lower())
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    filtered_sentence = [] 
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w) 
    # print(word_tokens) 
    # print("\n\n\nfilter ", filtered_sentence)
    print(sum('employee' in s for s in filtered_sentence)

    div = len(re.findall('DEVOPAM', text_string))
    
    m = re.search('employee', text_string, re.MULTILINE)  # Match
    # <re.Match object; span=(4, 5), match='X'>
    print(m)
    '''
    div = {"dividend" : 0, 'interim' : 0}
    bon = {"bonus" : 0, "bonus rights" : 0,"bonus shares" : 0, "bonus issue":0}
    ss = {"stock split": 0, "split":0}
    rss = {"reverse stock split":0, "reverse":0}
    rts = {"rights issue":0, "issue right":0 }
    mrgac = {"merger": 0, "mrgr":0, "acquir":0, "acquisition":0}
    emp = {"employee":0, "scheme":0}
    
    ca_dict = {"dividend": div, "bonus": bon, "stock split": ss, "reverse stock split": rss, "rights issue": rts, "merge and acquisition": mrgac, "employee": emp}

    ca_weight = {"dividend": 0, "bonus": 0, "stock split": 0, "reverse stock split": 0, "rights issue": 0, "merge and acquisition": 0,"employee": 0}

    for word, ca in ca_dict.items():
        for key in ca:
            ca[key] = text_string.count(word)
    for ca1 in ca_weight:
        values = ca_dict[ca1].values()
        ca_weight[ca1] = sum(values)
    return (str(max(ca_weight, key=ca_weight.get)))

def get_date():
    raw = parser.from_file('C:\\Temporary\\docs\\corporate_actions\\HU2.pdf')
    md = raw['metadata']
    print(md['date'])

def connect_database():
    try:
        conn = mysql.connector.connect(host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com',
                                        user='admin',
                                        password='SIH_2020',
                                        database='corporate_actions')
        if conn.is_connected():
            db_Info = conn.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = conn.cursor()
            cursor.execute("create database pythanos_main;")
            # cursor.execute('create database web_server;')
            cursor.execute("show databases")
            res = cursor.fetchall()
            print("Available databases: ", res)

    except Error as e:
        print("Error while connecting to MySQL", e)

    return(conn,cursor)


if __name__ == "__main__":
    conn,cursor = connect_database()
    print(conn)
    pdf_list = glob.glob("../next_gen/next_gen/full/*.pdf")
    for pdf in pdf_list:
        read_pdf(pdf)
        text_string = read_text_file()
        # nlp = spacy.load('en_core_web_lg')
        # doc = nlp(text_string)

        ca_name = get_ca_type(text_string)
        date = get_date()

        '''
        matches = []
        try:
            matches = list(datefinder.find_dates(text_string, index=True, strict=False))
            print((matches))
            for match in matches:
                print("match ",match)
        except TypeError:
            print ("TypeError")
        except:
            print("An unknown error occured")
        finally:
            #put dates in panda
            sorted_dates = sorted(matches)
            print(sorted_dates)
        
        matches = list(datefinder.find_dates(text_string, index=True, strict=False))
        print((matches))
        for match in matches:
            print("match ",match)
        sorted_dates = sorted(matches)
        print(sorted_dates) 
        
        '''
        sql = "CREATE TABLE IF NOT EXISTS dashboard (ca_name VARCHAR(20) NOT NULL, date VARCHAR(20), rec_date VARCHAR(20)"
        cursor.execute(sql)
        