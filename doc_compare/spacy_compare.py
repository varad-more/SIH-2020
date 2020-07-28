import numpy as np
from matplotlib import pyplot as plt

import gensim
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_multiple_whitespaces

from operator import itemgetter
import sqlite3
import pandas as pd
import sys
import spacy
spacy.prefer_gpu()
import operator
import time
import itertools

# Read sqlite query results into a pandas DataFrame #business-standards #reuters #moneycontrol
database_list=["reuters_new.sqlite","business-standards_new.sqlite","moneycontrol_new.sqlite"]
con = sqlite3.connect("/home/suraj/database_sih/"+database_list[0])
df=pd.read_sql_query("SELECT * from Articles", con)

for database in database_list[1:]:
    print(database)
    con = sqlite3.connect("/home/suraj/database_sih/"+database)
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
for message in messages:
    message = strip_punctuation(message)
    message = strip_multiple_whitespaces(message)
    stop_words_removed.append(remove_stopwords(message))
    #print(remove_stopwords(message))
print(len(messages))

removed_ttt=[]
for message in stop_words_removed:
    temp=""
    for m in message.split(" "):
        if m in ["t","tt","ttt","tttt","ttttt","tttttt","ttttttt","tttttttt","ttttttttt","r","rr","rrr","rrrr"]:
            continue        
        temp+=m+" "
    
    removed_ttt.append(temp)
stop_words_removed=removed_ttt


# sample text



print("-------------------------------------")
print(len(stop_words_removed))

message_embeddings_=None
corr=np.empty((len(stop_words_removed),len(stop_words_removed)))

model_location = "en_core_web_lg"

nlp = spacy.load(model_location)

#print(docs[0].similarity(docs[1])
#for i in range(len(docs)):
#    print(docs[0][0].similarity(docs[i][0]))
#print(len(docs))

def check_similarity(docs):
    return docs[0].similarity(docs[1])




start=time.time()
docs=list(nlp.pipe(stop_words_removed,500))
docs =list(map(operator.itemgetter(0), docs))
temp=list(itertools.product(docs, repeat=2))

output = list(map(check_similarity, temp))
corr=np.asarray(output).reshape((len(docs),len(docs)))
#df = pd.DataFrame(temp, columns =['a','b'])
print(time.time()-start)
#d=df.apply(check_similarity,axis=1)
#temp=np.asarray(temp).reshape((len(docs),len(docs)))
#print(len(temp))
#print(df)
#print(time.time()-start)

"""temp=np.asarray(temp)
print(temp)
print(type(temp))

for x,pair in enumerate(itertools.product(docs, repeat=2)):
    print(check_similarity(*pair))
    #print(x)
kj
for x,doc1 in enumerate(stop_words_removed):
    for y,doc2 in enumerate(stop_words_removed):
        corr[x,y]=check_similarity(doc1, doc2)
        print(x+y)
"""

threshold=0.90
print(corr.shape)
print(np.where(corr[0]>threshold)[0].tolist())

#print(messages[np.where(corr[0]>0.8)[0].tolist()])
print(len(messages))
print("############################################################################################################################")
already_checked=[]
nomatch=0
matching_articles=[]
with open("output.txt", "w") as file1:
    file1.write("##########################################----Testing New article-----####################################################"+"\n")
    for i in range(len(messages)):
        #print("!----!")
        #print(np.where(corr[i]>threshold))
        ##print("already_checked:",already_checked)
        ##print("check:",np.where(corr[i]>threshold)[0].tolist())
        if len(np.where(corr[i]>threshold)[0].tolist())>1:
            #print("----------------------All articles Below match with each other-------------------")
            file1.write("----------------------All articles Below match with each other-------------------"+"\n")
            for n,m in zip(np.where(corr[i]>threshold)[0].tolist(),itemgetter(*np.where(corr[i]>threshold)[0].tolist())(stop_words_removed)):
                ##print(n)
                if not (np.where(corr[i]>threshold)[0].tolist() in already_checked ):
                    #print("link of the below article :",links[n])
                    file1.write("link of the below article :"+links[n]+"   similarity : "+str(corr[i,n])+"\n")
                    #print("link of the below article :"+links[n]+"   similarity : "+str(corr[i,n])+"\n")
                    
                    #print(m)
                    file1.write(m+"\n")
                    #print("--------new matching article---------")
                    file1.write("--------new matching article---------"+"\n")
                else:
                    ##print("already checked this article")
                    break
            already_checked.append(np.where(corr[i]>threshold)[0].tolist())
        else:
            nomatch+=1
            n=np.where(corr[i]>threshold)[0].tolist()[0]
            #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!1!no match for this article!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #file1.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!no match for this article!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"+"\n")
            #print("link of the below article :",links[n])
            #file1.write("link of the below article :"+links[n]+"   similarity : "+str(corr[i,n])+"\n")
            loc=np.where(corr[i]>threshold)[0].tolist()[0]
            #print(messages[loc])
            #file1.write(messages[loc]+"\n")
        #print("################################################----Testing New article-----###################################################")
        file1.write("##########################################----Testing New article-----####################################################"+"\n")
        
#print(itemgetter(*np.where(corr[0]>0.8)[0].tolist())(messages))
print(time.time()-start)
print(nomatch)