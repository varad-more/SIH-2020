import tensorflow_hub as hub
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
import tensorflow
import os
import random
import gensim
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_multiple_whitespaces
from gensim.parsing.preprocessing import stem_text
from operator import itemgetter
import sqlite3
import pandas as pd
import sys
import time
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

def load_universal_encoder(module_url):
    print("--------------------------------------------------------------------------")
    embed = hub.Module(module_url)
    print("model loaded")
    return embed


def load_database(database_list=["financialexpress","moneycontrol","yahoo","reuters","livemint","marketwatch"]):
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
    articles_database["present"]=False
    articles_database["action"]=""  
    return articles_database





def cooperate_actions_lists_and_code(cooperate_action_list,cooperate_action_code):
    cooperate_action_list=[x.lower() for x in cooperate_action_list]
    cooperate_action_code=[x.lower() for x in cooperate_action_code]
    cooperate_action=pd.DataFrame(cooperate_action_list,columns=['CA'])
    cooperate_action["CA"]=cooperate_action["CA"].str.lower()
    return cooperate_action,cooperate_action_code



def find_actions(articles_database,cooperate_action,cooperate_action_code):

    for i in cooperate_action["CA"]:
        articles_database["present"]=articles_database["present"] | articles_database["content"].str.match(i, case=False)
        articles_database.loc[articles_database["content"].str.match(i, case=False),["action"]]+=","+i

    articles_database.reset_index(inplace = True)


    for i in cooperate_action_code:
        for num,sentence in enumerate(articles_database["content"]):
            if i in list(gensim.utils.tokenize(sentence)):
                articles_database.loc[num,['present']]=True
                articles_database.loc[num,['action']]+=","+i

    articles_database=articles_database.loc[articles_database["present"]]

    articles_database=articles_database.drop(articles_database[articles_database['present'] == False].index)
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



def run_universal_encoder(embed,stop_words_removed):
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
            else :
                message_embeddings_=np.append(message_embeddings_,session.run(similarity_message_encodings, feed_dict={similarity_input_placeholder: sentences}),axis=0)
                
        corr = np.inner(message_embeddings_, message_embeddings_)

    return corr
    

def write_output_file(corr,stop_words_removed):
    threshold=0.92
    already_checked=[]
    nomatch=0
    matching_articles=[]
    print(time.time()-start)
    with open("output.txt", "w") as file1:
        file1.write("##########################################----Testing New article-----####################################################"+"\n")
        for i in range(len(stop_words_removed)):
            if len(np.where(corr[i]>threshold)[0].tolist())>1:
                file1.write("----------------------All articles Below match with each other-------------------"+"\n")
                for n,m in zip(np.where(corr[i]>threshold)[0].tolist(),itemgetter(*np.where(corr[i]>threshold)[0].tolist())(stop_words_removed)):
                    if not (np.where(corr[i]>threshold)[0].tolist() in already_checked ):
                        file1.write("link of the below article :"+links[n]+"   similarity : "+str(corr[i,n])+"\n")
                        file1.write(m+"\n")
                        file1.write("--------new matching article---------"+"\n")
                    else:
                        break
                already_checked.append(np.where(corr[i]>threshold)[0].tolist())
            else:
                nomatch+=1
                n=np.where(corr[i]>threshold)[0].tolist()[0]
                loc=np.where(corr[i]>threshold)[0].tolist()[0]
            file1.write("##########################################----Testing New article-----####################################################"+"\n")
        
def initialize_CA_vars():
    cooperate_action_code=["ANN","ARR" ,"ASSM" ,"BB" 	,"BKRP" ,"BON" ,"BR" 	,#"CALL" 	,
                            "CAPRD" 	,"AGM" 	,"CONSD" 	,"CONV" 	,"CTX" 	,
                            "CURRD","DIST" 	,"DIV" 	, "DMRGR ","DRIP" ,"DVST" ,"ENT" 	,"FRANK" ,"FTT" 	,"FYCHG" ,                           
                            "ICC" 	,"INCHG" ,"ISCHG" ,"LAWST","LCC" ,"LIQ" 	,"LSTAT" ,"LTCHG" ,"MKCHG" ,"MRGR" 	,"NLIST" ,
                            "ODDLT","PID" ,"PO" ,"PRCHG" ,"PRF" ,"PVRD" 	,"RCAP"  ,"REDEM" ,	"RTS" ,"SCCHG" ,"SCSWP" ,
                            "SD" ,"SECRC" ,"TKOVR"]

    cooperate_action_list=[ "Announcement","Arrangement","Assimilation","Buy Back","Bankruptcy","Bonus Issue","Bonus Rights",
                                   # "Call",
                                    "Capital Reduction",
                                    "Company Meeting",
                                    "Consolidation" ,"stock split",
                                    "Conversion",
                                    "Certificate Exchange",
                                    "Currency Redenomination",
                                    "Distribution",
                                    "Dividend",
                                    "Demerger",
                                    "Dividend Reinvestment Plan",
                                    "Divestment",
                                    "Entitlements",
                                    "Franking",
                                    "Financial Transaction Tax",
                                    "Financial Year Change",
                                    "International Code Change",
                                    "Incorporation Change",
                                    "Issuer Name Change",
                                    "Lawsuit",
                                    "Local Code Change",
                                    "Liquidation",
                                    "Listing Status Change",
                                    "Lot Change",
                                    "Market Segment Change",
                                    "Merger",
                                    "New Listing",
                                    "Odd Lot Offer",
                                    "Property Income Distribution",
                                    "Purchase Offer",
                                    "Primary Exchange Change",
                                    "Preferential Offer",
                                    "Parvalue Redenomination",
                                    "Return of Capital",
                                    "Preference Redemption",
                                    "Rights",
                                    "Security Description Change",
                                    "Security Swap",
                                    "Subdivision",
                                    "Security Reclassification",
                                    "Takeover"]

    return cooperate_action_code,cooperate_action_list



if __name__ == "__main__":
    start=time.time()
    embed=load_universal_encoder("https://tfhub.dev/google/universal-sentence-encoder/1?tf-hub-format=compressed")
    articles_database=load_database()
    articles_database=clean_database(articles_database)
    cooperate_action_code,cooperate_action_list=initialize_CA_vars()
    cooperate_action,cooperate_action_code=cooperate_actions_lists_and_code(cooperate_action_list,cooperate_action_code)
    articles_database=find_actions(articles_database,cooperate_action,cooperate_action_code)
    links,stop_words_removed=remove_stopwords_from_database(articles_database)
    corr=run_universal_encoder(embed,stop_words_removed)
    write_output_file(corr,stop_words_removed)
    print(time.time()-start)
    for i in stop_words_removed:
        print(i)
        print("-----------------------------")

    for i,j,action in zip(articles_database["content"],articles_database["url"],articles_database["action"]):
        print("url:" +j)
        print("----------")
        print(i)
        print("----------")
        print("action:  ",action)
        print("##########################")