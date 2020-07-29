import numpy as np


import gensim
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_multiple_whitespaces
from gensim.parsing.preprocessing import stem_text


import sqlite3
import pandas as pd
import spacy
# spacy.prefer_gpu()

import operator
import time
import itertools
from sklearn import preprocessing


def load_database(database_list=["financialexpress","moneycontrol","yahoo","reuters","livemint","marketwatch","tenderfoot"]):
    con = sqlite3.connect("/home/suraj/database_sih/"+database_list[0]+".sqlite")
    articles_database=pd.read_sql_query("SELECT * from Articles", con)
    for database in database_list[1:]:
        con = sqlite3.connect("/home/suraj/database_sih/"+database+".sqlite")
        temp = pd.read_sql_query("SELECT * from Articles", con)
        articles_database=articles_database.append(temp)
    
    return articles_database

def clean_database(articles_database):
    articles_database=articles_database.iloc[articles_database['content'].notna().tolist()]
    articles_database=articles_database.iloc[articles_database['content'].notnull().tolist()]
    articles_database=articles_database.drop(articles_database[articles_database['content'] == ''].index)
    articles_database=articles_database[~articles_database['content'].duplicated()]
    articles_database['content']=articles_database['content'].str.lower()
    
    return articles_database

def remove_stopwords_from_database(articles_database):
    links=articles_database['url'].tolist()
    messages=articles_database['content'].tolist()
    stop_words_removed=[]

    for message in messages:
        message = strip_punctuation(message)
        message=stem_text(message)
        message = strip_multiple_whitespaces(message)
        stop_words_removed.append(remove_stopwords(message))
    return links,stop_words_removed


def check_similarity(docs):
    return docs[0].similarity(docs[1])


def run_spacy_similarity(stop_words_removed):

    model = "en_core_web_lg"
    nlp = spacy.load(model)
    docs=list(nlp.pipe(stop_words_removed,500))
    docs =list(map(operator.itemgetter(0), docs))
    temp=list(itertools.product(docs, repeat=2))
    output = list(map(check_similarity, temp))
    corr=np.asarray(output).reshape((len(docs),len(docs)))
    return corr


def cosine_similarity(stop_words_removed):

    model = "en_core_web_lg"

    nlp = spacy.load(model)
    docs=list(nlp.pipe(stop_words_removed,500))
    docs =list(map(operator.itemgetter(0), docs))
    vectors=np.empty((0,300))

    for doc in docs:
        vectors=np.append(vectors,[doc.vector],axis=0)

    vectors = preprocessing.normalize(vectors, norm='l2')          
    corr = np.inner(vectors, vectors)
    
    return corr
    



def write_output_file(corr,stop_words_removed,links):
    threshold=0.90
    already_checked=[]
    nomatch=0
    
    with open("output.txt", "w") as file1:
        file1.write("##########################################----Testing New article-----####################################################"+"\n")
        for i in range(len(stop_words_removed)):
            if len(np.where(corr[i]>threshold)[0].tolist())>1:
                file1.write("----------------------All articles Below match with each other-------------------"+"\n")
                for n,m in zip(np.where(corr[i]>threshold)[0].tolist(),operator.itemgetter(*np.where(corr[i]>threshold)[0].tolist())(stop_words_removed)):
                    if not (np.where(corr[i]>threshold)[0].tolist() in already_checked ):
                        file1.write("link of the below article :"+links[n]+"   similarity : "+str(corr[i,n])+"\n")
                        file1.write(m+"\n")
                        file1.write("--------new matching article---------"+"\n")
                    else:
                        break
                already_checked.append(np.where(corr[i]>threshold)[0].tolist())
            else:
                nomatch+=1
                
                #n=np.where(corr[i]>threshold)[0].tolist()[0]
                #loc=np.where(corr[i]>threshold)[0].tolist()[0]
            file1.write("##########################################----Testing New article-----####################################################"+"\n")
            

if __name__ == "__main__":
    
    articles_database=load_database(["tenderfoot","tenderfoot_three"])
    articles_database=clean_database(articles_database)
    links,stop_words_removed=remove_stopwords_from_database(articles_database)
    corr=run_spacy_similarity(stop_words_removed)
    
    #corr=cosine_similarity(stop_words_removed)
    write_output_file(corr,stop_words_removed,links)
