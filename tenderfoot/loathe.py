"""Loathe module

This module is the final ranker for the CA scraping bot.
"""

__version__ = '4'
__author__ = 'Abhijit Acharya'

import sys
import mysql.connector
from datetime import datetime

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


class Loathe(object):
    """Loathe class ranks the urls"""

    def __init__(self):
        print(text_color.HEADER_COLOR
              + "Initialized loathe object"
              + text_color.ENDC)
        super(Loathe, self).__init__()

    # Connect to database
    def connect_database(self):
        try:
            self.connection = mysql.connector.connect(
                     host="database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com",
                     user="admin",
                     password="SIH_2020",
                     database="pythanos_main"
                   )

            # self.connection = sqlite3.connect('output/tenderfoot.sqlite')
            self.cursor = self.connection.cursor(buffered=True)
            print(text_color.GREEN_COLOR
                  + "Connected to database"
                  + text_color.ENDC)
        except Exception as ex:
            print(text_color.FAILED_COLOR
                  + error_string.format(ex)
                  + text_color.ENDC)
            sys.exit(0)

    # # Load models
    # def load_models(self):
    #     try:
    #         self.model = load_model('models/best_model.h5')
    #     except Exception as ex:
    #         print(text_color.FAILED_COLOR
    #               + error_string.format(ex)
    #               + text_color.ENDC)

    # loop over articles and rank
    def loop_over_articles_and_rank(self):
        try:
            while True:
                self.cursor.execute('SELECT articles.id,articles.url,articles.publish_date,pages.filename,pages.website,pages.new_rank FROM articles INNER JOIN pages ON articles.id=pages.pages_id WHERE articles.content is NOT NULL and articles.error is NULL LIMIT 1')
                row = self.cursor.fetchone()
                print(row[1])
                self.cursor.execute('SELECT name,web_rank FROM webs WHERE name=%s LIMIT 1', (row[4],))
                webs = self.cursor.fetchone()
                print("HERE")
                website_name = webs[0]
                web_rank = webs[1]
                if row[2] != None:
                    old_date = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
                    with open('output/dumps/'+row[3],'r', encoding='utf-8') as f:
                        try:
                            html_str = f.read()
                            article.download(html_str)
                            article.parse()
                            new_date = datetime.strptime(article.publish_date, '%Y-%m-%d %H:%M:%S')
                            if old_date != new_date:
                                self.cursor.execute('UPDATE webs SET web_rank=%s WHERE website=%s', (int(web_rank)-0.3, website_name))
                        except Exception as ex:
                            print(ex)
                        finally:
                            f.close()

        except Exception as ex:
            self.connection.commit()
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    # Close connection
    def close_cur(self):
        try:
            self.cursor.close()
            print("Connection closed")
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    def loathe(self):
        self.connect_database()
        # self.load_models()
        self.loop_over_articles_and_rank()
        self.close_cur()
