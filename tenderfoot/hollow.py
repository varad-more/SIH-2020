"""Hollow module

This module is the parser for the CA scraping bot.
"""

__version__ = '1'
__author__ = 'Abhijit Acharya'

import sys
import json
import html
import string
import sqlite3
import mysql.connector
from time import sleep
from newspaper import Article
from bs4 import BeautifulSoup

error_string = """
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n
Exception : {}\n
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n
"""

class text_color:
    HEADER_COLOR = '\033[95m'
    BLUE_COLOR = '\033[94m'
    GREEN_COLOR = '\033[92m'
    WARNING_COLOR = '\033[93m'
    FAILED_COLOR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Hollow(object):
    """This class provides methods for parsing data from links"""

    def __init__(self, arg, starturl):
        super(Hollow, self).__init__()
        # escapes = ''.join([chr(char) for char in range(1, 32)])
        # self.translator = str.maketrans('', '', escapes)
        self.companies = list(dict.fromkeys(['hexaware', 'coca', 'intel', 'cola', 'suzuki','snapdeal', 'shopclues', 'nissan', 'volkswagen', 'airtel', 'lg', 'air india', 'airbus', 'daimler', 'donohoe', 'samsung', 'walmart', 'hitachi', 'siemens', 'wilmar', 'endurance', 'lloyds', 'bp', 'bpcl', 'google', 'petrochina', 'petronet', 'jio', 'britannia', 'nippon', 'pepsi', 'pepsico', 'fiat', 'waymo', 'chrysler', 'kfc', 'goldman', 'boeing', 'amazon', 'lodha', 'flipkart' ,'Bharat' , 'lnt', 'lti', 'toubro', 'larsen', 'paytm', 'forge', 'sachs', 'acc', 'apollo', 'tyre', 'ashok', 'leyland', 'aban', 'offshore', 'abbott', 'abg', 'shipyard', 'adani', 'enterprises', 'aditya', 'birla', 'nuvo', 'aftek', 'aia', 'alembic', 'alfa', 'laval', 'allsec', 'alok', 'alstom', 'anant', 'raj', 'amara', 'raja', 'batteries', 'amtek', 'ansal', 'spacex', 'properties', 'infrastructure', 'asahi', 'glass', 'electronics', 'star', 'astrazeneca', 'atlas', 'copco', 'aurobindo', 'axles', 'mitsubishi', 'aventis', 'abb', 'ltd', 'aventis', 'crop', 'atcom', 'atco', 'adlabs', 'films', 'atn', 'electricals', 'ballarpur', 'balmer', 'lawrie', 'balrampur', 'chini', 'mills', 'bannari', 'amman', 'sugars', 'bata', 'berger', 'paints', 'bharat', 'bijlee', 'bharat', 'earth', 'movers', 'bharat', 'forge', 'bharat', 'heavy', 'electricals', 'bharat', 'bhushan', 'strips', 'binani', 'blue', 'dart', 'express', 'bombay', 'rayon', 'fashions', 'bongaigaon', 'refinery', 'bosch', 'chassis', 'systems', 'bharat', 'electronics', 'birla', 'nvidia', 'tesla', 'britannia', 'biocon', 'bsel', 'infrastructure', 'realty', 'baffin', 'bajaj', 'hindustan', 'carborundum', 'universal', 'castrol', 'chambal', 'fertiliser', 'ccl', 'century', 'plyboards', 'century', 'container', 'corporation', 'coromandel', 'clariant', 'classic', 'diamonds', 'colgate', 'palmolive', 'country', 'club', 'cranes', 'softwares', 'crew', 'bos', 'cummins', 'cadila', 'crompton', 'greaves', 'cesc', 'chemplast', 'sanmar', 'cinevista', 'creative', 'eye', 'crest', 'crisil', 'cummins', 'cybermate', 'infotek', 'cyberspace', 'dabur', 'dalmia', 'cements', 'dynamatic', 'dewan', 'corp', 'dishman', "divi's", 'laboratories', 'donear', 'dredging', 'kulkarni', 'developers', 'silk', 'educomp', 'elder', 'elecon', 'electrosteel', 'castings', 'esab', 'essar', 'shipping', 'essar', 'everest', 'kanto', 'cylinder', 'exide', 'eicher', 'motor', 'emami', 'parry', 'electrolux', 'kelvinator', 'elgitread', 'eskay', 'essel', 'propack', 'etc', 'eveready', 'excel', 'travancore', 'finolex', 'flex', 'force', 'motors', 'fag', 'bearings', 'fcl', 'fdc', 'finolex', 'cables', 'forbes', 'gokak', 'framatome', 'frontier', 'fujitsu', 'icim', 'gateway', 'distriparks', 'gemini', 'genus', 'overseas', 'electronics', 'geodesic', 'systems', 'geojit', 'geometric', 'software', 'solution', 'glaxosmithkline', 'consumers', 'glenmark', 'gmr', 'godrej', 'consumers', 'godrej', 'graphite', 'grasim', 'great', 'shipping', 'greaves', 'cotton', 'greenply', 'grindwell', 'norton', 'gruh', 'ambuja', 'cement', 'gas', 'co.', 'state', 'chem.', 'gulf', 'gail', 'gammon', 'gillette', 'havell', 'helios', 'matheson', 'himadri', 'inds.', 'hindalco', 'hinduja', 'tmt', 'hindustan', 'hindustan', 'glass', 'hindustan', 'sanitaryware', 'inds', 'hindustan', 'zinc', 'honeywell', 'apple', 'leela', 'hcl', 'hdfc', 'hero', 'honda', 'motors', 'hindustan', 'lever', 'hindustan', 'machine', 'tools', 'ht', 'igate', 'il&fs', 'investmart', 'cements', 'hotels', 'petrochemicals', 'corp', 'indraprastha', 'enterprises', 'ingersoll-rand', 'ipca', 'laboratories', 'itd', 'cementation', 'ig', 'petrochemicals', 'ivrcl', 'infrastructures', 'infosys', 'cement', 'jain', 'jaiprakash', 'associates', 'jammu', 'kashmir', 'jaybharat', 'real', 'jb', 'jbf', 'jindal', 'saw', 'jindal', 'stainless', 'jindal', 'jk', 'cements', 'jm', 'jmc', 'jsw', 'jubilant', 'organosys', 'jyoti', 'structures', 'jet', 'airways', 'kajaria', 'ceramics', 'kalpataru', 'transmission', 'kansai', 'nerolac', 'paints', 'kei', 'kemrock', 'exports', 'kennametal', 'kesoram', 'kirloskar', 'brothers', 'kirloskar', 'engines', 'kirloskar', 'pneumatic', 'ksb', 'pumps', 'kotak', 'mahindra', 'ksl', 'realty', 'infrastructure', 'lakshmi', 'foods', 'lakshmi', 'machine', 'works', 'lic', 'lumax', 'madras', 'aluminium', 'madras', 'cements', 'mahanagar', 'telephone', 'mahindra', 'gesco', 'developers', 'mahindra', 'ugine', 'mangalam', 'cement', 'manugraph', 'marg', 'maruti', 'udyog', 'mcleod', 'russel', 'mcnally', 'bharat', 'mercator', 'moser', 'baer', 'motherson', 'sumi', 'systems', 'motor', 'mrf', 'mastek', 'max', 'megasoft', 'merck', 'mrpl', 'nagarjuna', 'nagarjuna', 'nahar', 'spinning', 'mills', 'aluminium', 'fertilizer', 'nava', 'bharat', 'nestle', 'nicholas', 'piramal', 'nrb', 'bearings', 'nucleus', 'software', 'exports', 'niit', 'ntpc', 'ocl', 'opto', 'circuits', 'ongc', 'prithvi', 'procter', 'gamble', 'hygiene', 'provogue', 'rajshree', 'sugars', 'ramsarup', 'ranbaxy', 'laboratories', 'rashtriya', 'chemicals', 'fertilizers', 'ratnamani', 'tubes', 'reliance', 'rolta', 'ruchi', 'soya', 'radico', 'khaitan', 'raymond', 'plant', 'sakthi', 'sugars', 'sangam', 'sanghi', 'satyam', 'computer', 'shipping', 'simplex', 'infrastructures', 'solectron', 'centum', 'electronics', 'marine', 'engg', 'iron', 'spanco', 'telesystems', 'srei', 'infrastructure', 'sterlite', 'sterlite', 'optical', 'strides', 'arcolab', 'suashish', 'diamonds', 'subex', 'azure', 'subhash', 'sujana', 'sun', 'surana', 'authority', 'elxsi', 'tata', 'tcs', 'tea', 'techno', 'electric', 'television', 'eighteen', 'torrent', 'transport', 'triveni', 'tube', 'tulip', 'titan', 'tvs', 'motor', 'spirits', 'usha', 'martin', 'uttam', 'galva', 'vaibhav', 'gems', 'videocon', 'videsh', 'sanchar', 'nigam', 'voltas', 'vakrangee', 'softwares', 'varun', 'shipping', 'walchandnagar', 'welspun', 'stahl', 'rohren', 'wockhardt', 'wipro', 'yes']))
        self.arg = arg
        self.starturl = starturl
        print(text_color.HEADER_COLOR + "Initialized hollow object" + text_color.ENDC)

    # Remove punctuations
    def preprocessing(self,line):
        # line = line.translate(self.translator)

        puncts = ""
        for i in string.punctuation:
            if i!="%" and i!="$" and i!="/" and i!=":":
                puncts += i
        spaces = "".join([" "]*28)
        line = line.translate(str.maketrans(puncts,spaces))
        line = line.lower().split(' ')

        if "copyright" in line:
            return "NONE"

        if "subscriber" in line:
            return "NONE"

        return " ".join(line)

    # Get company names in keywords
    def get_company(self,keywords):
        spaces = "".join([" "]*32)
        keywords = keywords.translate(str.maketrans(string.punctuation,spaces)).lower()
        company = []
        #######################################################################
        for j in self.companies:
            for i in keywords.split(" "):
                if j == i:
                    company.append(j)
        #######################################################################
        if company==[]:
            return "NULL"
        return list(dict.fromkeys(company))

    # Connect to table or create tables if not already done
    def connect_to_existing_table_or_create(self):
        try:
            # Connect to database
            self.connection = mysql.connector.connect(
              host="localhost",
              user="root",
              password="Abhijit@123",
              database="deadpan"
            )
            # self.connection = mysql.connector.connect(
            #          host="database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com",
            #          user="admin",
            #          password="SIH_2020",
            #          database="pythanos_main"
            #        )
            # self.connection = mysql.connector.connect(
            #           host="database-1.ce0yosk0xfgx.us-east-1.rds.amazonaws.com",
            #           user="admin",
            #           password="SIH_2020",
            #           database="database1"
            #         )

            # self.connection = sqlite3.connect('output/tenderfoot.sqlite')
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute('SELECT web_rank from webs WHERE url=%s LIMIT 1',(self.starturl,))
            row = self.cursor.fetchone()
            self.web_rank = row[0]
            print(text_color.GREEN_COLOR + "Connected to database " + 'tenderfoot' + text_color.ENDC)

            # Creates the main table
            self.cursor.execute('''
                                    CREATE TABLE IF NOT EXISTS pages
                                    (
                                        id INT PRIMARY KEY auto_increment,
                                        url varchar(1000) UNIQUE,
                                        keywords varchar(5000),
                                        website varchar(5000),
                                        error INT,
                                        old_rank FLOAT,
                                        new_rank FLOAT,
                                        moved INT,
                                        filename varchar(500)
                                    );
                                ''')

            # Many to many tableId,url,title,keywords,content,author,publish_date,old_rank,new_rank,error
            self.cursor.execute('''
                                    CREATE TABLE IF NOT EXISTS links
                                    (
                                        from_id INT,
                                        to_id INT,
                                        UNIQUE(from_id, to_id)
                                    );
                                ''')

            # website main links, for site based ranking
            self.cursor.execute('''
                                    CREATE TABLE IF NOT EXISTS webs
                                    (
                                        name varchar(100),
                                        url varchar(1000) UNIQUE,
                                        web_rank FLOAT
                                    );
                                ''')

            # Error table, for error logging
            self.cursor.execute('''
                                    CREATE TABLE IF NOT EXISTS errors
                                    (
                                        url varchar(1000) UNIQUE,
                                        exception varchar(2000)
                                    );
                                ''')

            # Drained data table
            self.cursor.execute('''
                                    CREATE TABLE IF NOT EXISTS articles
                                    (
                                        id INT PRIMARY KEY auto_increment,
                                        url varchar(1000) UNIQUE,
                                        company_name varchar(500),
                                        error INT,
                                        authors varchar(1000),
                                        publish_date varchar(1000),
                                        title varchar(1000),
                                        content varchar(10000),
                                        keywords varchar(5000),
                                        filename varchar(5000),
                                        ranks FLOAT
                                    );
                                ''')

        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)
            sys.exit(0)

    # Check to see if we are already in progress...
    def check_if_already_in_progress(self):
        try:
            # Get id and url of empty keywords' rows
            self.cursor.execute('INSERT INTO articles(id, url, keywords, filename) SELECT pages_id, url, keywords, filename FROM pages WHERE keywords is NOT NULL and keywords != "NULL" and keywords != "" and moved = 0;')
            self.cursor.execute('UPDATE pages SET moved=%s WHERE keywords is NOT NULL and keywords != "NULL" and keywords != ""',(1,))
            self.connection.commit()
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    # get link and parse html
    def get_link_and_drain(self):
        try:
            counter = 0
            s = '\|/-'
            t = iter(s)
            l=0
            while True:
                l+=1
                # Get id and url of empty html
                self.cursor.execute('SELECT id,url,keywords,filename FROM articles WHERE content is NULL and error is NULL ORDER BY ranks LIMIT 1')
                try:
                    if counter==4:
                        counter=0
                        t=iter(s)
                    counter+=1
                    row = self.cursor.fetchone()
                    company_names = self.get_company(row[2])

                    # Get one article and hollow it
                    article = Article(row[1])
                    # Get html from dump
                    with open('output/dumps/'+row[3],'r', encoding='utf-8') as f:
                        try:
                            # data = json.load(f)
                            # html_str = data[str(row[0])]
                            html_str = f.read()
                        except Exception as ex:
                            print(ex)
                        finally:
                            f.close()

                    try:
                        # html from file
                        article.download(html_str)
                    except:
                        # download the article
                        article.download()
                    article.parse()

                    content_text = self.preprocessing(str(article.text))
                    # print(content_text)
                    if content_text == "NONE":
                        self.cursor.execute('UPDATE articles SET error=%s WHERE url=%s',(-1,row[1]))
                        continue

                    # Remove anythong less than 50 chars...
                    if len(article.text)>50:
                        self.cursor.execute('UPDATE articles SET authors=%s, publish_date=%s, title=%s, content=%s, company_name=%s WHERE url=%s', (str(article.authors), article.publish_date, article.title, content_text[:9999], str(company_names), row[1]))
                        # self.cursor.execute('UPDATE webs SET web_rank=%s WHERE url=%s',(int(self.web_rank)+0,self.starturl))
                    else:
                        self.cursor.execute('UPDATE articles SET error=%s WHERE url=%s',(-1,row[1]))
                        # self.cursor.execute('UPDATE webs SET web_rank=%s WHERE url=%s',(int(self.web_rank)-0,self.starturl))

                    sys.stdout.write('\rloading {} {}'.format(next(t),l))
                except Exception as ex:
                    # All done for today
                    sys.stdout.write('\rDone!!                                                     ')
                    print(ex)
                    print(text_color.FAILED_COLOR + 'No undrained HTML articles found' + text_color.ENDC)
                    break
                self.connection.commit()

        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    # Close connection
    def close_cur(self):
        try:
            self.cursor.close()
            print(text_color.GREEN_COLOR + "Connection closed" + text_color.ENDC)
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    # Main spider
    def drain(self):
        self.connect_to_existing_table_or_create()
        self.check_if_already_in_progress()
        self.get_link_and_drain()
        self.close_cur()
