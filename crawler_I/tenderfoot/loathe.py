"""Loathe module

This module is the final ranker for the CA scraping bot.
"""

__version__ = '4'
__author__ = 'Abhijit Acharya'

import sys
import time
import sqlite3
import numpy as np
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
            self.connection = sqlite3.connect("output/tenderfoot.sqlite")
            self.cursor = self.connection.cursor()
            print(text_color.GREEN_COLOR + "Connected to database" + text_color.ENDC)
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)
            sys.exit(0)

    # Load models from pickle
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
                self.cursor.execute('SELECT Articles.id,Articles.url,Articles.content,Pages.new_rank FROM Articles INNER JOIN Pages ON Articles.id=Pages.id WHERE Articles.content is NOT NULL and Articles.rank is NULL and Articles.error is NULL ORDER BY Pages.new_rank LIMIT 1')
                row = self.cursor.fetchone()
                streeng = [[row[2]]]
                tokenizer.fit_on_texts(list(streeng))
                x_tr_seq  = tokenizer.texts_to_sequences(streeng)
                x_tr_seq  = pad_sequences(x_tr_seq, maxlen=100)
                new_rank_value = self.model.predict_proba(x_tr_seq)[0][0]
                self.cursor.execute('UPDATE Articles SET rank=? WHERE url=?', (float(new_rank_value),row[1]) )
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
