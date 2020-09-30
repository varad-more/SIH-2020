
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Script to collect and find similar articles from the database and rank the 
# sites providing them by the order of reliability using fuzzy logic
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import tensorflow_hub as hub
import numpy as np
import tensorflow
import os
import gensim
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_multiple_whitespaces
from gensim.parsing.preprocessing import strip_numeric
#from gensim.parsing.preprocessing import stem_text
from operator import itemgetter
#import sqlite3
import pandas as pd
import time
from sklearn import preprocessing
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import random,time
import itertools
import requests
from io  import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import mysql.connector
#import urllib.request as urllib2
import ssl
import re
import spacy
#python -m spacy download en_core_web_lg
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"



class Article_matcher():
    def __init__(self,module_url):
        self.cooperate_action_code,self.cooperate_action_list=self.initialize_CA_vars()
        self.embed=self.load_universal_encoder(module_url)
        self.connect_database()
        self.connect_websever()
        self.company_spacy = spacy.load("en_core_web_lg")
        
    def __del__(self):
        self.mycursor.close()
        self.mydb.close()

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Initializing the list of CA codes and event types in a dictionary format
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  
    def initialize_CA_vars(self):
        cooperate_action_code=["ANN","ARR" ,"ASSM"	,"BKRP" ,"BR" ,
                                "CAPRD" 	,"AGM" 	,"CONSD" 	,"CONV" 	,"CTX" 	,
                                "CURRD","DIST" 	,"DIV" 	, "DMRGR ","DRIP" ,"DVST" ,                           
                                "INCHG" ,"ISCHG" ,"LAWST","LCC" ,"LIQ" 	,"LSTAT" ,"LTCHG" ,"MKCHG" ,"MRGR" 	,"NLIST" ,
                                "ODDLT" ,"PRCHG" ,"PRF" ,"PVRD","RCAP"  ,"REDEM" ,	"RTS" ,"SCCHG" ,"SCSWP" ,
                                "SECRC" ,"TKOVR"]

        cooperate_action_list=["Acquisition","Bonus Issue","Bonus Rights","Cash Dividend",
                                    "Final Redemption","General Announcement",
                                    "Name Change","Optional Dividend","Partial Redemption",
                                    "Par Value Change","Reverse Stock Split","Rights Auction","Rights Issue",
                                    "Scrip Dividend","Scrip Issue","Spin-Off","Spin Off","Stock Dividend","Subscription Offer","Tender Offer",
                                    "Warrant Exercise","Warrant Expiry","Warrant Issue","annual general meeting",
                                        "Capital Reduction",
                                        "Company Meeting","board meeting"
                                        "Consolidation" ,"stock split","stock-split",
                                        "Distribution",
                                        "Dividend",
                                        "Demerger",
                                        "Dividend Reinvestment Plan",
                                        "Divestment",
                                        "Entitlements",
                                        "Issuer Name Change",
                                        "Lawsuit",
                                        "Listing Status Change",
                                        "Lot Change",
                                        "Merger",
                                        "New Listing",
                                        "Preferential Offer",
                                        "Parvalue Redenomination",
                                        "Return of Capital",
                                        "Preference Redemption",
                                        "Security Description Change",
                                        "Subdivision",
                                        "Takeover","Equity","Debt"]

        return cooperate_action_code,cooperate_action_list

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Loading and executing the universal Google encoder script for NLP
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 
    def load_universal_encoder(self,module_url):
        print("--------------------------------loading_model------------------------------------------")
        embed = hub.Module(module_url)
        print("model loaded")
        return embed
    
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Connecting to RDS database 'pythanos_main'
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def connect_database(self):
        self.mydb = mysql.connector.connect(host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com',
                                         database='pythanos_main',
                                         user='admin',
                                         password='SIH_2020')

        self.mycursor = self.mydb.cursor()
    
    def connect_websever(self):
        self.webserver_db = mysql.connector.connect(host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com',
                                         database='web_server',
                                         user='admin',
                                         password='SIH_2020')

        self.webserver_mycursor = self.webserver_db.cursor()
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Extract content, url, ranks & company name associated with the articles
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>        
    def get_articles(self):
        #self.mycursor.execute("SELECT id,url,content,ranks FROM articles where news_checked is NULL and content is not NULL")
        self.mycursor.execute("SELECT id,url,content,ranks,company_keywords,keywords FROM articles where news_checked is NULL and content is not NULL limit 10")
        articles_database = pd.DataFrame(self.mycursor.fetchall(),columns=["id","url","content","ranks","company_name","keywords"])
        self.mycursor.execute("UPDATE articles set news_checked=0 where news_checked is NULL")
        self.mydb.commit()
        #self.webserver_mycursor.execute("SELECT link FROM dashboard_latest_news limit 100")
      #  print(self.webserver_mycursor.fetchall)
        for i in articles_database["url"].tolist():
            print(i)
            self.webserver_mycursor.execute("UPDATE dashboard_latest_news set link=%s,repetition=%s",(i,"0"))
            print("-")
        print(articles_database)
        self.webserver_db.commit()
        time.sleep(1)
        self.webserver_mycursor.execute("SELECT link FROM dashboard_latest_news")
        print(self.webserver_mycursor.fetchall())
        
        return articles_database
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Updating the verification status, CA name after running the encoder model
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def update_articles_table(self,articles_database):
        print("updating database")
        for company,action,url,matches,rank,keywords in zip(articles_database["company_name"],articles_database["action"].tolist(),articles_database["url"].tolist(),articles_database["matches"].tolist(),articles_database["ranks"].tolist(),articles_database["keywords"].tolist()):
            #print("updating database")
            print(type(company),type(action),type(url),type(matches),type(rank),type(keywords))
            a=(" ".join(company),matches,action,rank,url)
            print(a)
            self.mycursor.execute("UPDATE articles set company_keywords=%s,news_checked=%s,ca_name=%s,ranks=%s WHERE news_checked=0 and url=%s",a)
            self.webserver_mycursor.execute("UPDATE dashboard_latest_news set repetition=%s,headline=%s WHERE link=%s",(matches,keywords,url))
        #self.mycursor.execute("UPDATE crawler_2 set ca_checked=1 where ca_checked=0")
        self.mydb.commit()
        self.webserver_db.commit()
        print("database updated")

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Data Frame for organizing the content, CA, Company name in articles_database
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def clean_database(self,articles_database):
        articles_database=articles_database.iloc[articles_database['content'].notna().tolist()]
        
        articles_database=articles_database.iloc[articles_database['content'].notnull().tolist()]
        
        articles_database=articles_database.drop(articles_database[articles_database['content'] == ''].index)
        
        articles_database=articles_database[~articles_database['content'].duplicated()]
        
        articles_database['content']=articles_database['content'].str.lower()
        
        articles_database["present"]=False
        articles_database["action"]="" 
        
        return articles_database

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Coperate actions lists and codes taken as dataframe
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    
    def cooperate_actions_lists_and_code(self,cooperate_action_list,cooperate_action_code):
        
        cooperate_action_list=[x.lower() for x in cooperate_action_list]
        
        cooperate_action_code=[x.lower() for x in cooperate_action_code]
        
        cooperate_action=pd.DataFrame(cooperate_action_list,columns=['CA'])
        
        cooperate_action["CA"]=cooperate_action["CA"].str.lower()
        
        return cooperate_action,cooperate_action_code

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Get company name
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    
    def get_company(self, keywords):
            tagged_text = self.company_spacy(keywords)
            extracted_entities = [(i.text, i.label_) for i in tagged_text.ents]
            company = []
            for j in extracted_entities:
                if j[1]=="ORG" and j[0].lower()!="coronavirus" and j[0].lower()!="isis" and j[0].lower()!="covid" and j[0].lower()!="gold" and j[0].lower()!="goa" :
                    company.append(j[0])
            if company==[]:
                return ""
            return company


    def check_company_names(self,articles_database):
        articles_database["company_name"]=""
        articles_database["company_name"]=articles_database["keywords"].apply(self.get_company)
        articles_database=articles_database.loc[articles_database["company_name"].str.len()>0]
        #articles_database=articles_database.loc[articles_database["action"].str.len()>0]
        print("articles database updated")
        print(articles_database["company_name"])

        return articles_database


    def find_actions(self,articles_database,cooperate_action,cooperate_action_code):
        articles_database["action"]="" 
        articles_database["content"]=articles_database["content"].map(str)

        for i in cooperate_action["CA"]:
 
            articles_database["present"]=articles_database["present"] | articles_database["content"].str.contains(i, case=False)
            
            articles_database.loc[articles_database["content"].str.contains(i, case=False),["action"]]+=","+i
            
        articles_database.reset_index(inplace = True)

        for i in cooperate_action_code:
            for num,sentence in enumerate(articles_database["content"]):
                if i in list(gensim.utils.tokenize(sentence)):
                    articles_database.loc[num,['present']]=True
                    articles_database.loc[num,['action']]+=","+i
        
        articles_database=articles_database.loc[articles_database["present"]]
        print(articles_database)
        print("---")
        print(articles_database)
        return articles_database

    
    def get_CA_info(self,articles_database):
        print("H----------------------------------------------------------------------------------------------------------H")
        articles_database=articles_database.loc[articles_database["present"]]
        nlp = spacy.load("ca_extractor_dividend")
        print(articles_database)
        articles_database.action = articles_database.action.str[1:]
        for ca,url,content in zip(articles_database["action"],articles_database["url"],articles_database["content"]):
            if "dividend" in ca:
                doc2 = nlp(content)   
                z=1
                x=1
                ca_type=""
                rec_date=""
                for ent in doc2.ents:
                    if ent.label_=="ca_type" and z:
                        ca_type=" ca type: "+ent.text
                        z=0
                    if ent.label_=="rec_date" and x:
                        rec_date=" rec date :"+ent.text
                        x=0
                    if x==0 and z==0:        
                        
                        self.webserver_mycursor.execute("UPDATE dashboard_latest_news set ner_summary=%s WHERE link=%s",(ca_type+rec_date,url))
                        print(ca_type+rec_date,url)
                        break
            else :
                doc2=self.company_spacy(content)
                for ent in doc2.ents:
                    if ent.label_=="DATE":
                        print("---")
                        self.webserver_mycursor.execute("UPDATE dashboard_latest_news set ner_summary=%s WHERE link=%s",(ca+" rec_date:"+ent.text,url))
                        print(ca+" rec_date:"+ent.text,url)
                        break
                        
        self.webserver_db.commit()
        
    def company_name_security_master(self):
        self.mycursor.execute("SELECT name_of_company FROM security_master")
        company_name=pd.DataFrame(self.mycursor.fetchall())
        company_name.columns=["name"]
        company_name=company_name[~company_name['name'].duplicated()]
        print(company_name)


    def remove_stopwords_from_database(self,articles_database):
        links=articles_database['url'].tolist()
        messages=articles_database['content'].tolist()
        CA_names=articles_database['action'].tolist()
        stop_words_removed=[]

        for message in messages:
            message = strip_punctuation(message)
            #message=stem_text(message)
            message = strip_multiple_whitespaces(message)
            message=strip_numeric(message)
            stop_words_removed.append(remove_stopwords(message))
        
        return links,stop_words_removed,CA_names


    def run_universal_encoder(self,stop_words_removed):

        similarity_input_placeholder = tensorflow.placeholder(tensorflow.string, shape=(None))
        similarity_message_encodings = self.embed(similarity_input_placeholder)
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
            message_embeddings_ = preprocessing.normalize(message_embeddings_, norm='l2')          
            corr = np.inner(message_embeddings_, message_embeddings_)
        print(corr)
        return corr
    
    def check_matching_count_of_articles(self,articles_database,corr,stop_words_removed,links,threshold=0.92):
        already_checked=[]
        articles_database["matches"]=0
        for i in range(len(stop_words_removed)):
                if len(np.where(corr[i]>threshold)[0].tolist())>1:
                    for n,m in zip(np.where(corr[i]>threshold)[0].tolist(),itemgetter(*np.where(corr[i]>threshold)[0].tolist())(stop_words_removed)):
                        articles_database.loc[articles_database.url.str.contains(links[n],case=False),"matches"]=len(np.where(corr[i]>threshold)[0].tolist())
                        articles_database.loc[articles_database.url.str.contains(links[n],case=False),"ranks"]=len(np.where(corr[i]>threshold)[0].tolist())*0.6+0.4*articles_database.loc[articles_database.url.str.contains(links[n],case=False),"ranks"]
                        #print(articles_database.loc[np.where(corr[i]>threshold)[0].tolist(),"content"])
                        #j
                else:
                    n=np.where(corr[i]>threshold)[0].tolist()[0]
                    articles_database.loc[articles_database.url.str.contains(links[n],case=False),"matches"]=1                    
        print("----------------")
        articles_database.action = articles_database.action.str[1:]
        print(articles_database.loc[articles_database['matches'] > 1,["content","company_name","matches","action"]])
        temp=articles_database.where(articles_database['matches'] < 1).dropna()
        for content,action,matches in zip(temp["content"],temp["action"],temp["matches"]):
            #print(type(i))
            #print(i[0])

            #print(action+"matches:"+str(matches)+"\n"+content)
            print("------------------------")

        return articles_database


    def write_output_file(self,corr,stop_words_removed,links,CA_names,threshold=0.93):
        already_checked=[]
        nomatch=0
        print(time.time()-start)
        with open("output.txt", "w") as file1:
            file1.write("##########################################----Testing New article-----####################################################"+"\n")
            for i in range(len(stop_words_removed)):
                if len(np.where(corr[i]>threshold)[0].tolist())>1:
                    file1.write("----------------------All articles Below match with each other-------------------"+"\n")
                    for n,m in zip(np.where(corr[i]>threshold)[0].tolist(),itemgetter(*np.where(corr[i]>threshold)[0].tolist())(stop_words_removed)):
                        if not (np.where(corr[i]>threshold)[0].tolist() in already_checked ):
                            file1.write("link of the below article :"+links[n]+"   CAs found : "+CA_names[n]+"   similarity : "+str(corr[i,n])+"\n")
                            file1.write(m+"\n")
                            file1.write("--------new matching article---------"+"\n")
                        else:
                            break
                    already_checked.append(np.where(corr[i]>threshold)[0].tolist())
                else:
                    nomatch+=1
                    n=np.where(corr[i]>threshold)[0].tolist()[0]
                    loc=np.where(corr[i]>threshold)[0].tolist()[0]
                    file1.write("---------------------------No match------------------------")
                    file1.write("link of the below article :"+links[n]+"   CAs found : "+CA_names[n]+"   similarity : "+str(corr[i,n])+"\n")
                    file1.write(itemgetter(*np.where(corr[i]>threshold)[0].tolist())(stop_words_removed)+"\n")
                    file1.write("--------------------------------------------------------")
                    
                file1.write("##########################################----Testing New article-----####################################################"+"\n")
    
    def get_pdf_links(self):
        self.mycursor.execute("SELECT file_url FROM crawler_2 where url_error=0 and ca_checked is NULL limit 10")
        pdf_links = pd.DataFrame(self.mycursor.fetchall())
        #self.mydb.commit()
        if len(pdf_links)==0:
            return []
        pdf_links=pdf_links[0].tolist()
        print("pdf links:",len(pdf_links))
        return pdf_links
    

    def pdf_to_text(self,path):
        pagenums = set()
        output = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)
        infile = open(path, 'rb')
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
        infile.close()
        converter.close()
        text = output.getvalue()
        output.close

        return text

    
    def read_pdfs(self):
        #context = ssl._create_unverified_context()
        pdf_links=self.get_pdf_links()
        if len(pdf_links)==0:
            print("no links")
            return 
        pdf_data= pd.DataFrame()
        pdf_data["content"]=""
        pdf_data["present"]=""
        pdf_data["action"]=""
        pdf_data["url"]=""
        print(len(pdf_links))
        for link in pdf_links:
            try:
            #pdf= urllib2.urlopen(link,context=context)
                r = requests.get(link,verify=False,stream=True,timeout=(5,20))
                with open(link+'.pdf', 'wb') as fd:
                    for chunk in r.iter_content(2000):
                        fd.write(chunk)
                print(link)
                pdf=self.pdf_to_text("data.pdf")
                pdf_data=pdf_data.append({"content":strip_multiple_whitespaces(pdf),"url":link},ignore_index=True)
                print("------------------------------")
                self.mycursor.execute("UPDATE crawler_2 set ca_checked=0 WHERE file_url=%s",(link,))
            except:
                self.mycursor.execute("UPDATE crawler_2 set url_error=1 WHERE file_url=%s",(link,))
                print("couldn't download from "+link)

            self.mydb.commit()
        return pdf_data  

    def run_article_matching(self):
        
        #articles_database=self.load_database(["tenderfoot","tenderfoot_three"])
        articles_database=self.get_articles()
        if len(articles_database)==0:
            print("no articles found")
            return
        articles_database=self.clean_database(articles_database)
        cooperate_action_code,cooperate_action_list=self.initialize_CA_vars()
        cooperate_action,cooperate_action_code=self.cooperate_actions_lists_and_code(self.cooperate_action_list,self.cooperate_action_code)
        articles_database=self.check_company_names(articles_database)
        articles_database=self.find_actions(articles_database,cooperate_action,cooperate_action_code)
        self.get_CA_info(articles_database)
        print(articles_database)
        links,stop_words_removed,CA_names=self.remove_stopwords_from_database(articles_database)
        corr=self.run_universal_encoder(stop_words_removed)
        articles_database=self.check_matching_count_of_articles(articles_database,corr,stop_words_removed,links,threshold=0.95)
        self.update_articles_table(articles_database)
        #self.write_output_file(corr,stop_words_removed,links,CA_names)
        
        return articles_database
    
    def update_pdf_database(self,pdf_data):

        for i,j in zip(pdf_data["action"].tolist(),pdf_data["url"].tolist()):
            a=(i,j)
            print(a)
            self.mycursor.execute("UPDATE crawler_2 set ca_type=%s WHERE file_url=%s",a)
        self.mycursor.execute("UPDATE crawler_2 set ca_checked=1 where ca_checked=0")
        self.mydb.commit()
        
    def reset_database(self):
        self.mycursor.execute("UPDATE articles set news_checked=NULL")
        self.mycursor.execute("UPDATE crawler_2 set ca_checked=NULL")
        self.mydb.commit()

    def run_pdf_data_extraction(self):
        pdf_data=self.read_pdfs()
        if pdf_data is None:
            print("no pdf")
            return 
        cooperate_action,cooperate_action_code=self.cooperate_actions_lists_and_code(self.cooperate_action_list,self.cooperate_action_code)
        pdf_data=self.find_actions(pdf_data,cooperate_action,cooperate_action_code)
        self.update_pdf_database(pdf_data)
        
        """
        print(pdf_data)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        for present,action,content in zip(pdf_data["present"],pdf_data["action"],pdf_data['content']):
            print(content)
            print("\n ---------------------------------------")
            if present:
                print("action found : "+ action+ "\n"+"content:\n"+content+"\n-----------------------------")
        """


    def fuzzy_logic(self):
        quality = ctrl.Antecedent(np.arange(0, 100, 1), 'suraj')
        service = ctrl.Antecedent(np.arange(0, 100, 1), 'abhijit')
        prev_score =  ctrl.Antecedent(np.arange(0, 100, 1), 'prev_score')
        score = ctrl.Consequent(np.arange(0, 100, 0.1), 'score')

        quality.automf(3)
        service.automf(3)
        prev_score.automf(3)
        
        # Triangle
        score['low'] = fuzz.trimf(score.universe, [0, 0, 25])
        score['medium'] = fuzz.trimf(score.universe, [25, 37.5, 50])
        score['fairly-medium'] = fuzz.trimf(score.universe, [ 50, 62.5,75])
        score['high'] = fuzz.trimf(score.universe, [75,100, 100])

        rule1 = ctrl.Rule(quality['poor'] | service['poor'] | prev_score['poor'] , score['low'])
        rule2 = ctrl.Rule(service['average'] | prev_score['average'] | quality['average'], score['medium'])
        rule3 = ctrl.Rule(service['poor'] | prev_score['average'] | quality['average'], score['fairly-medium'])
        rule4 = ctrl.Rule(service['good'] | quality['good'] | prev_score['good'], score['high'])

        self.scoring_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])

    def calc(self,quality,service,prev_score):
        scoring = ctrl.ControlSystemSimulation(self.scoring_ctrl)

        scoring.input['suraj'] = quality
        scoring.input['abhijit'] = service
        scoring.input['prev_score'] = prev_score
        scoring.compute()

        print (scoring.output['score'])

if __name__ == "__main__":
    start=time.time()
    while True:
       # try:
        #    matcher=Article_matcher("https://tfhub.dev/google/universal-sentence-encoder/4")
            matcher=Article_matcher("https://tfhub.dev/google/universal-sentence-encoder-large/3")
            #matcher=Article_matcher("https://tfhub.dev/google/universal-sentence-encoder/1?tf-hub-format=compressed")
            break
        #except :
        #    time.sleep(1)
         #   continue
    print("database_connected")   
    while True:
        #matcher.company_name_security_master()
        matcher.reset_database()
        articles_database=matcher.run_article_matching()
    #    pdf_data=matcher.run_pdf_data_extraction()
        print(time.time()-start)
        start=time.time()
    
    """
    matcher.fuzzy_logic()
    quality = 100 #float(random.randint(0,11))
    service = 100 #float(random.randint(0,11))
    prev_score = 0 # Prev score
    matcher.calc(quality,service,prev_score)
    
    print(time.time()-start)
    articles_database=pdf_data
    with open("dataset.txt", "w") as file1:
        for i,j,action in zip(articles_database["content"],articles_database["url"],articles_database["action"]):
            file1.write("link:"+j+"    Action :  "+action+"\n")
            file1.write(i)
            #print(i)
            file1.write("----------------------------- \n \n \n ")

    for present,i,j,action in zip(articles_database["present"],articles_database["content"],articles_database["url"],articles_database["action"]):
        if present:
            print("url:" +j)
            print("----------")
            print(i)
            print("----------")
            print("action:  ",action)
            print("##########################")
    """
