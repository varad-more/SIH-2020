import tensorflow_hub as hub
import numpy as np
import tensorflow
import os
import gensim
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_multiple_whitespaces
#from gensim.parsing.preprocessing import stem_text
from operator import itemgetter
import sqlite3
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
import urllib.request as urllib2
import ssl
        
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

class Article_matcher():
    def __init__(self,module_url):
        self.cooperate_action_code,self.cooperate_action_list=self.initialize_CA_vars()
        self.embed=self.load_universal_encoder(module_url)
        self.connect_database()
        
    def __del__(self):
        self.mycursor.close()
        self.mydb.close()

    def initialize_CA_vars(self):
        cooperate_action_code=["ANN","ARR" ,"ASSM" ,"BB" 	,"BKRP" ,"BON" ,"BR" 	,#"CALL" 	,
                                "CAPRD" 	,"AGM" 	,"CONSD" 	,"CONV" 	,"CTX" 	,
                                "CURRD","DIST" 	,"DIV" 	, "DMRGR ","DRIP" ,"DVST" ,"ENT" 	,"FRANK" ,"FTT" 	,"FYCHG" ,                           
                                "ICC" 	,"INCHG" ,"ISCHG" ,"LAWST","LCC" ,"LIQ" 	,"LSTAT" ,"LTCHG" ,"MKCHG" ,"MRGR" 	,"NLIST" ,
                                "ODDLT","PID" ,"PO" ,"PRCHG" ,"PRF" ,"PVRD" 	,"RCAP"  ,"REDEM" ,	"RTS" ,"SCCHG" ,"SCSWP" ,
                                "SD" ,"SECRC" ,"TKOVR"]

        cooperate_action_list=[ "Announcement","Arrangement","Assimilation","Buy Back","Bankruptcy","Bonus","Bonus Issue","Bonus Rights",
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
                                        "Takeover","Equity"]

        return cooperate_action_code,cooperate_action_list

    def set_exclude_variable(self):
        self.exclude=["allotment"]
        
    def load_universal_encoder(self,module_url):
        print("--------------------------------loading_model------------------------------------------")
        embed = hub.Module(module_url)
        print("model loaded")
        return embed


    def load_database(self,database_list=["financialexpress","moneycontrol","yahoo","reuters","livemint","marketwatch","tenderfoot"]):
        con = sqlite3.connect("/home/suraj/database_sih/"+database_list[0]+".sqlite")
        articles_database=pd.read_sql_query("SELECT * from Articles", con)
        for database in database_list[1:]:
            con = sqlite3.connect("/home/suraj/database_sih/"+database+".sqlite")
            temp = pd.read_sql_query("SELECT * from Articles", con)
            articles_database=articles_database.append(temp)
        
        return articles_database

    def connect_database(self):
        
        self.mydb = mysql.connector.connect(host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com',
                                         database='pythanos_main',
                                         user='admin',
                                         password='SIH_2020')

        self.mycursor = self.mydb.cursor()
        
        
    def get_articles(self):
        self.mycursor.execute("SELECT * FROM articles ")
        articles_database = pd.DataFrame(self.mycursor.fetchall())
        #articles_database.columns = self.mycursor.keys()
        print(articles_database)
        g
        return articles_database



    def clean_database(self,articles_database):
        articles_database=articles_database.iloc[articles_database['content'].notna().tolist()]
        
        articles_database=articles_database.iloc[articles_database['content'].notnull().tolist()]
        
        articles_database=articles_database.drop(articles_database[articles_database['content'] == ''].index)
        
        articles_database=articles_database[~articles_database['content'].duplicated()]
        
        articles_database['content']=articles_database['content'].str.lower()
        
        articles_database["present"]=False
        articles_database["action"]="" 
        
        return articles_database

    def cooperate_actions_lists_and_code(self,cooperate_action_list,cooperate_action_code):
        
        cooperate_action_list=[x.lower() for x in cooperate_action_list]
        
        cooperate_action_code=[x.lower() for x in cooperate_action_code]
        
        cooperate_action=pd.DataFrame(cooperate_action_list,columns=['CA'])
        
        cooperate_action["CA"]=cooperate_action["CA"].str.lower()
        
        return cooperate_action,cooperate_action_code



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
        
        #articles_database=articles_database.loc[articles_database["present"]]
        
        return articles_database

    def get_CA_info(self,articles_database):
        articles_database=articles_database.loc[articles_database["present"]]
        for ca in articles_database:

            pass
            

    def remove_stopwords_from_database(self,articles_database):
        links=articles_database['url'].tolist()
        messages=articles_database['content'].tolist()
        CA_names=articles_database['action'].tolist()
        stop_words_removed=[]

        for message in messages:
            message = strip_punctuation(message)
            #message=stem_text(message)
            message = strip_multiple_whitespaces(message)
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
        return corr
    

    def write_output_file(self,corr,stop_words_removed,links,CA_names):
        threshold=0.92
        already_checked=[]
        nomatch=0
        #matching_articles=[]
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
        self.mycursor.execute("SELECT file_url FROM crawler_2 where ca_checked is NULL")
        pdf_links = pd.DataFrame(self.mycursor.fetchall())
        self.mycursor.execute("UPDATE crawler_2 set ca_checked=0 where ca_checked is NULL")
        pdf_links=pdf_links[0].tolist()
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
        for link in pdf_links[1:5]:
            try:
            #pdf= urllib2.urlopen(link,context=context)
                r = requests.get(link,verify=False,stream=True)
                with open('data.pdf', 'wb') as fd:
                    for chunk in r.iter_content(2000):
                        fd.write(chunk)
                print(link)
                pdf=self.pdf_to_text("data.pdf")
                pdf_data=pdf_data.append({"content":strip_multiple_whitespaces(pdf),"url":link},ignore_index=True)
                print("------------------------------")
            except:
                print("couldn't download from "+link)
        return pdf_data  

    def run_article_matching(self):
        
        #articles_database=self.load_database(["tenderfoot","tenderfoot_three"])
        articles_database=self.get_articles()
        articles_database=self.clean_database(articles_database)
        cooperate_action_code,cooperate_action_list=self.initialize_CA_vars()
        cooperate_action,cooperate_action_code=self.cooperate_actions_lists_and_code(self.cooperate_action_list,self.cooperate_action_code)
        articles_database=self.find_actions(articles_database,cooperate_action,cooperate_action_code)
        links,stop_words_removed,CA_names=self.remove_stopwords_from_database(articles_database)
        corr=self.run_universal_encoder(stop_words_removed)
        self.write_output_file(corr,stop_words_removed,links,CA_names)
        #self.run_stanford_word_2_vec(stop_words_removed=stop_words_removed)
        return articles_database
    
    def update_pdf_database(self,pdf_data):

        for i,j in zip(pdf_data["action"].tolist(),pdf_data["url"].tolist()):
            a=(i,j)
            print(a)
            self.mycursor.execute("UPDATE crawler_2 set ca_type=%s WHERE file_url=%s",a)
        self.mycursor.execute("UPDATE crawler_2 set ca_checked=1 where ca_checked=0")
        


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
    matcher=Article_matcher("https://tfhub.dev/google/universal-sentence-encoder/1?tf-hub-format=compressed")
    #while True:
        #articles_database=matcher.run_article_matching()
    pdf_data=matcher.run_pdf_data_extraction()
    
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