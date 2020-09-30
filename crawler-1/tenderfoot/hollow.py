"""Hollow module

This module is the parser for the CA scraping bot.
"""

import sys
import string
import mysql.connector
from newspaper import Article

error_string = """
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n
ERROR in {} : {}\n
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

    def __init__(self,connection,cursor):
        super(Hollow, self).__init__()
        self.connection = connection
        self.cursor = cursor
        print(text_color.HEADER_COLOR + "Initialized hollow object" + text_color.ENDC)

    # Remove punctuations
    def preprocessing(self, line):
        puncts = ""
        for i in string.punctuation:
            if i != "%" and i != "$" and i != "/" and i != ":":
                puncts += i
        spaces = "".join([" "]*28)
        line = line.translate(str.maketrans(puncts, spaces))
        line = line.lower().split(' ')

        if "copyright" in line:
            return "NONE"

        if "subscriber" in line:
            return "NONE"

        return " ".join(line)

    # Get company names in keywords
    def get_company(self, keywords):
        tagged_text = self.company_spacy(keywords)
        extracted_entities = [(i.text, i.label_) for i in tagged_text.ents]
        company = []
        for j in extracted_entities:
            if j[1]=="ORG" and j[0].lower()!="coronavirus" and j[0].lower()!="isis" and j[0].lower()!="covid":
                company.append(j[0])
        if company==[]:
            return "NULL"
        return company

    # Connect to table or create tables if not already done
    def connect_to_existing_table_or_create(self):
        try:
            # Connect to database
            self.connection = mysql.connector.connect(
                     host="database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com",
                     user="admin",
                     password="SIH_2020",
                     database="pythanos_main"
                   )

            self.cursor = self.connection.cursor(buffered=True)
            print(text_color.GREEN_COLOR + "Connected to database " + 'tenderfoot' + text_color.ENDC)

        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format("", ex) + text_color.ENDC)
            sys.exit(0)

    # Check to see if we are already in progress...
    def check_if_already_in_progress(self):
        try:
            # Get id and url of empty keywords' rows
            self.cursor.execute('''INSERT INTO articles(id, url, keywords, filename) SELECT pages_id, url, keywords, filename FROM pages WHERE keywords is NOT NULL and keywords != "NULL" and keywords != "" and moved = 0;''')
            self.cursor.execute('''UPDATE pages SET moved=%s WHERE keywords is NOT NULL and keywords != "NULL" and keywords != ""''', (1,))
            self.connection.commit()
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format("", ex) + text_color.ENDC)

    # get link and parse html
    def get_link_and_drain(self):
        try:
            counter = 0
            s = '\|/-'
            t = iter(s)
            l = 0
            while True:
                l += 1
                # Get id and url of empty html
                self.cursor.execute('''SELECT id,url,keywords,filename
                                      FROM articles WHERE content is NULL and
                                      error is NULL ORDER BY ranks LIMIT 1''')
                try:
                    if counter == 4:
                        counter = 0
                        t = iter(s)
                    counter += 1
                    row = self.cursor.fetchone()
                    company_names = self.get_company(row[2])

                    # Get one article and hollow it
                    article = Article(row[1])
                    # Get html from dump
                    with open('output/dumps/'+row[3],'r', encoding='utf-8') as f:
                        try:
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
                    if content_text == "NONE":
                        self.cursor.execute('''UPDATE articles SET error=%s WHERE url=%s''', (-1, row[1]))
                        continue

                    # Remove anythong less than 50 chars...
                    if len(article.text) > 50:
                        self.cursor.execute('''UPDATE articles SET authors=%s,
                                            publish_date=%s, title=%s,
                                            content=%s, company_name=%s
                                            WHERE url=%s''', (str(article.authors), article.publish_date, article.title, content_text[:9999], str(company_names), row[1]))
                    else:
                        self.cursor.execute('''UPDATE articles SET error=%s WHERE url=%s''', (-1, row[1]))

                    sys.stdout.write('\rloading {} {}'.format(next(t), l))
                except Exception as ex:
                    # All done for today
                    sys.stdout.write('\rDone!!      ')
                    print(ex)
                    print(text_color.FAILED_COLOR
                          + 'No undrained HTML articles found'
                          + text_color.ENDC)
                    break
                self.connection.commit()

        except Exception as ex:
            print(text_color.FAILED_COLOR
                  + error_string.format("", ex)
                  + text_color.ENDC)

    # Close connection
    def close_cur(self):
        try:
            self.cursor.close()
            print(text_color.GREEN_COLOR
                  + "Connection closed"
                  + text_color.ENDC)
        except Exception as ex:
            print(text_color.FAILED_COLOR
                  + error_string.format("", ex)
                  + text_color.ENDC)

    # Main spider
    def drain(self):
        self.check_if_already_in_progress()
        self.get_link_and_drain()
