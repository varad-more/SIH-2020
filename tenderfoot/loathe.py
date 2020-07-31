"""Loathe module

This module is the final ranker for the CA scraping bot.
"""

__version__ = '4'
__author__ = 'Abhijit Acharya'

import sys
import time
import sqlite3
import numpy as np
import mysql.connector
from collections import Counter
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

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
        print(text_color.HEADER_COLOR + "Initialized loathe object" + text_color.ENDC)
        super(Loathe, self).__init__()

    # Connect to database
    def connect_database(self):
        try:
            # self.connection = mysql.connector.connect(
            #   host="localhost",
            #   user="root",
            #   password="Abhijit@123",
            #   database="deadpan"
            # )
            self.connection = mysql.connector.connect(
                     host="database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com",
                     user="admin",
                     password="SIH_2020",
                     database="pythanos_main"
                   )
            # self.connection = mysql.connector.connect(
            #           host="database-1.ce0yosk0xfgx.us-east-1.rds.amazonaws.com",
            #           user="admin",
            #           password="SIH_2020",
            #           database="database1"
            #         )

            # self.connection = sqlite3.connect('output/tenderfoot.sqlite')
            self.cursor = self.connection.cursor(buffered=True)
            print(text_color.GREEN_COLOR + "Connected to database" + text_color.ENDC)
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)
            sys.exit(0)

    # Load models
    def load_models(self):
        try:
            self.model = load_model('models/best_model.h5')
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    # loop over articles and classify
    def loop_over_articles_and_classify(self):
        tokenizer = Tokenizer()
        try:
            while True:
                self.cursor.execute('SELECT articles.id,articles.url,articles.content,pages.new_rank FROM articles INNER JOIN pages ON articles.id=pages.pages_id WHERE articles.content is NOT NULL and articles.ranks is NULL and articles.error is NULL ORDER BY pages.new_rank LIMIT 1')
                row = self.cursor.fetchone()
                streeng = [[row[2]]]
                tokenizer.fit_on_texts(list(streeng))
                x_tr_seq  = tokenizer.texts_to_sequences(streeng)
                x_tr_seq  = pad_sequences(x_tr_seq, maxlen=100)
                new_rank_value = self.model.predict_proba(x_tr_seq)[0][0]
                self.cursor.execute('UPDATE articles SET ranks=%s WHERE url=%s', (float(new_rank_value),row[1]) )
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
        self.load_models()
        self.loop_over_articles_and_classify()
        self.close_cur()
