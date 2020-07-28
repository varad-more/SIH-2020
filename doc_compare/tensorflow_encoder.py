import tensorflow_hub as hub
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

import tensorflow
#import tensorflow.compat.v1 as tensorflow
#tensorflow.disable_v2_behavior()
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

#config = ConfigProto()
#config.gpu_options.allow_growth = True
#session = InteractiveSession(config=config)
import gensim
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_multiple_whitespaces
from gensim.parsing.preprocessing import stem_text

from operator import itemgetter
import sqlite3
import pandas as pd

import sys
#curl -L "https://tfhub.dev/google/universal-sentence-encoder-large/3?tf-hub-format=compressed" | tar -zxvC .
np.set_printoptions(threshold=sys.maxsize)
model_location = "/home/suraj/model_sih/"
print("loading model from location "+ model_location)
#embed = hub.load(model_location)

print("--------------------------------------------------------------------------")
module_url = "https://tfhub.dev/google/universal-sentence-encoder/1?tf-hub-format=compressed"
embed = hub.Module(module_url)
print("model loaded")

# Read sqlite query results into a pandas DataFrame #business-standards #reuters #moneycontrol
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

for message in messages:
    message = strip_punctuation(message)
    message=stem_text(message)
    message = strip_multiple_whitespaces(message)
    stop_words_removed.append(remove_stopwords(message))
    #print(remove_stopwords(message))
print(len(messages))

removed_ttt=[]
for message in stop_words_removed:
    temp=""
    for m in message.split(" "):
        if m in ["t","tt","ttt","tttt","ttttt","tttttt","ttttttt","tttttttt","ttttttttt","r","rr","rrr","rrrr"]:
            print(m)
            continue        
        temp+=m+" "
    
    removed_ttt.append(temp)
print(removed_ttt)
stop_words_removed=removed_ttt
import time
start=time.time()


print("-------------------------------------")
print(len(stop_words_removed))

similarity_input_placeholder = tensorflow.placeholder(tensorflow.string, shape=(None))
similarity_message_encodings = embed(similarity_input_placeholder)
corr=None
message_embeddings_=None
chunks = [stop_words_removed[x:x+1000] for x in range(0, len(stop_words_removed), 1000)]
with tensorflow.Session() as session:
    session.run(tensorflow.global_variables_initializer())
    session.run(tensorflow.tables_initializer())

    for sentences in chunks:
        if message_embeddings_ is None :
            message_embeddings_ = session.run(similarity_message_encodings, feed_dict={similarity_input_placeholder: sentences})
            print(message_embeddings_.shape)
        else :
            message_embeddings_=np.append(message_embeddings_,session.run(similarity_message_encodings, feed_dict={similarity_input_placeholder: sentences}),axis=0)
            print(message_embeddings_.shape)
    print(message_embeddings_.shape)
    print(type(message_embeddings_))
    corr = np.inner(message_embeddings_, message_embeddings_)
    #print(corr)
    #heatmap(messages, messages, corr)
#print(corr.shape)
#print(np.where(corr[0]>0.8))
print(message_embeddings_.shape,len(stop_words_removed))
threshold=0.92
print(np.where(corr[0]>threshold)[0].tolist())

#print(messages[np.where(corr[0]>0.8)[0].tolist()])
print(len(messages))
print("############################################################################################################################")
already_checked=[]
nomatch=0
matching_articles=[]
print(time.time()-start)
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
print(time.time()-start)