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
for message in stop_words_removed:
    temp=""
    for m in message.split(" "):
        if m in ["t","tt","ttt","tttt","ttttt","tttttt","ttttttt","tttttttt","ttttttttt","r","rr","rrr","rrrr"]:
            continue        
        temp+=m+" "
    
    removed_ttt.append(temp)
stop_words_removed=removed_ttt

#import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(stop_words_removed)
dense_array=vectors.toarray()
#print(vectors.toarray().shape)

corr=np.inner(dense_array,dense_array)
#print(dense_array[0])
"""
#feature_names = vectorizer.get_feature_names()
#dense = vectors.todense()
#denselist = dense.tolist()
#df = pd.DataFrame(denselist, columns=feature_names)

from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess
dictionary = Dictionary()
doc_tokenized = [simple_preprocess(doc) for doc in stop_words_removed]
BoW_corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in doc_tokenized]
tfidf = TfidfModel(BoW_corpus, smartirs='ntc')
print("----")
print(tfidf)
print(BoW_corpus)
features=[]
for i in range(len(stop_words_removed)):
    features.append(tfidf[BoW_corpus[i]])
    print(len(features))

print(features[0])
print(features[1254])
j    
print(features)
array=df.to_numpy()

print(array)
print(array.shape)
corr = np.inner(array, array)
"""
threshold=0.8
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
print(nomatch)