from gensim import corpora, models, similarities
import jieba
import numpy as np
from matplotlib import pyplot as plt

import gensim
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_multiple_whitespaces
from gensim.parsing.preprocessing import strip_numeric

from operator import itemgetter
import sqlite3
import pandas as pd


database_list=["business-standards","cnbc","financialexpress","livemint","marketwatch","moneycontrol","reuters"]
con = sqlite3.connect("/home/suraj/database_sih/"+database_list[0]+".sqlite")
df=pd.read_sql_query("SELECT * from Articles", con)

for database in database_list[1:]:
    print(database)
    con = sqlite3.connect("/home/suraj/database_sih/"+database+".sqlite")
    temp = pd.read_sql_query("SELECT * from Articles", con)
    df=df.append(temp)
    print(df)

# Verify that result of SQL query is stored in the dataframe
print(df)
#df=df[df['content']==""]
#print(type(df['content'].notna()))
print("-----------------------")
df=df.iloc[df['content'].notna().tolist()]
print(len(df))
df=df.iloc[df['content'].notnull().tolist()]
print(len(df))
df=df.drop(df[df['content'] == ''].index)
print(len(df))
df=df[~ df['content'].duplicated()]
print(df)
print(len(df))
print("-----------------------")

links=df['url'].tolist()
messages=df['content'].tolist()
stop_words_removed=[]
from gensim.parsing.preprocessing import stem_text
for message in messages:
    message=strip_numeric(message)
    message=stem_text(message)
    message = strip_punctuation(message)
    message = strip_multiple_whitespaces(message)
    stop_words_removed.append(remove_stopwords(message))
    #print(remove_stopwords(message))
print(len(messages))

removed_ttt=[]
"""for message in stop_words_removed:
    temp=""
    for m in message.split(" "):
        if m in ["t","tt","ttt","tttt","ttttt","tttttt","ttttttt","tttttttt","ttttttttt","r","rr","rrr","rrrr"]:
            continue        
        temp+=m+" "
    
    removed_ttt.append(temp)
stop_words_removed=removed_ttt
"""
stop_words_removed = [jieba.lcut(text) for text in stop_words_removed]
dictionary = corpora.Dictionary(stop_words_removed)
feature_cnt = len(dictionary.token2id)
corpus = [dictionary.doc2bow(text) for text in stop_words_removed]
tfidf = models.TfidfModel(corpus)
arr=np.empty((len(stop_words_removed),len(stop_words_removed)))
for l,words in enumerate(stop_words_removed):
    kw_vector = dictionary.doc2bow(jieba.lcut(words[0]))
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features = feature_cnt)
    sim = index[tfidf[kw_vector]]
    arr[l,:]=sim
    print(l)
print(arr)

