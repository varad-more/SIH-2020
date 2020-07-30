import mysql.connector
import re
from mysql.connector import Error

try:
    conn = mysql.connector.connect(host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com',
                                         user='admin',
                                         password='SIH_2020')
    if conn.is_connected():
        db_Info = conn.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = conn.cursor()
        cursor.execute("create database corporate_actions;")
        cursor.execute('create database web_server;')
        cursor.execute("show databases")
        res = cursor.fetchall()
        print("Available databases: ", res)

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    cursor.close()

try:
    conn = mysql.connector.connect(host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com',
                                         database='corporate_actions',
                                         user='admin',
                                         password='SIH_2020')
    if conn.is_connected():
        db_Info = conn.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchall()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)

cursor = conn.cursor()

# found = False

# for db in cursor:
#     pattern = "[(,')]"
#     db_string = re.sub(pattern,"", str(db))
#     if(db_string == 'fis_2'):
#         found = True
#         print("database fis_2 exists")
#         cursor.execute("use fis_2")

#     if(not found):
#         cursor.execute("CREATE database fis_2")
#         cursor.execute("use fis_2")


# sql = "DROP TABLE IF EXISTS Articles"
# cursor.execute(sql)
# sql = "DROP TABLE IF EXISTS Pages"
# cursor.execute(sql)
# sql = "DROP TABLE IF EXISTS Company"
# cursor.execute(sql)
# sql = "DROP TABLE IF EXISTS Securities"
# cursor.execute(sql)
# sql = "DROP TABLE IF EXISTS Table_1"
# cursor.execute(sql)
# sql = "DROP TABLE IF EXISTS Dashboard"
# cursor.execute(sql)
# sql = "DROP TABLE IF EXISTS Websites"
# cursor.execute(sql)

##Articles
sql = "CREATE TABLE IF NOT EXISTS Articles (article_id INT AUTO_INCREMENT PRIMARY KEY,article_url VARCHAR(30),article_title VARCHAR(30),article_keywords VARCHAR(30),article_content VARCHAR(30),article_author VARCHAR(30),article_old_rank int NOT NULL,article_new_rank int NOT NULL,article_error VARCHAR(5),article_verified BOOLEAN NULL)"
cursor.execute(sql)
##table created

# cursor.execute("INSERT INTO Articles (article_id, article_url, article_title, article_keywords, article_content, article_author, article_old_rank, article_new_rank, article_error) VALUES('1','url','title','keywords','content','author','2','4','error')")

##Pages
sql = "CREATE TABLE IF NOT EXISTS Pages (page_id int NOT NULL,page_url VARCHAR(30),page_keywords VARCHAR(30),page_old_rank int NOT NULL,page_new_rank int NOT NULL)"
# sql = "CREATE TABLE IF NOT EXISTS Pages (page_id int NOT NULL,page_url VARCHAR(30),page_keywords VARCHAR(30),page_old_rank int NOT NULL,page_new_rank int NOT NULL, FORIEGN KEY (page_id) REFERENCES Articles(article_id))"

cursor.execute(sql)

# cursor.execute("INSERT INTO Pages (page_id ,page_url, page_keywords, page_old_rank, page_new_rank) VALUES ('1','url','keywords','2','4')")

##Websites
sql = "CREATE TABLE IF NOT EXISTS Websites (web_id int NOT NULL,web_url VARCHAR(30),web_old_rank int NOT NULL,web_new_rank int NOT NULL)"
cursor.execute(sql)

# cursor.execute("INSERT INTO Websites (web_id, web_url, web_old_rank, web_new_rank) VALUES ('1','url','2','4')")

##Company
sql = "CREATE TABLE IF NOT EXISTS Company (company_name TEXT NULL,securities_ex VARCHAR(10),company_web_link VARCHAR(30),op_timeline VARCHAR(10),trading_location VARCHAR(10))"
cursor.execute(sql)

# cursor.execute("INSERT INTO Company (company_name, securities_ex, company_web_link, op_timeline, trading_location) VALUES ('Jio','a','b','c','d')")

##Securities
sql = "CREATE TABLE IF NOT EXISTS Securities ( ID int NOT NULL,company_name TEXT NULL,security_type VARCHAR(10),ISIN VARCHAR(10),trade_volume TEXT NOT NULL,listed_on_exchange VARCHAR(20),Exchange_symbol VARCHAR(10),PRIMARY KEY (ID), FOREIGN KEY (ID) REFERENCES Articles(article_Id))"
cursor.execute(sql)

# cursor.execute("INSERT INTO Securities (security_type,ISIN, trade_volume,listed_on_exchange,Exchange_symbol) VALUES ('e','f','1','g','h')")

##Table_1
sql = "CREATE TABLE IF NOT EXISTS Table_1 (ID TEXT NOT NULL,company_name TEXT NULL,parent_link VARCHAR(20),file_url VARCHAR(20))" #,publish_date VARCHAR(5))" 
# publish date removal and varchar 300.
cursor.execute(sql)

# cursor.execute("INSERT INTO Table_1 (parent_link,file_url,publish_date) VALUES ('e','f','1')")

##Dashboard
sql = "CREATE TABLE IF NOT EXISTS Dashboard (date_ca TEXT NULL,company_name TEXT NULL,ca_name TEXT NULL,security_id_type TEXT NULL,id_value TEXT NULL,ex_date TEXT NULL,rec_date TEXT NULL,pay_date TEXT NULL, other VARCHAR(30),exception BOOLEAN NULL,remarks VARCHAR(10))"
cursor.execute(sql)

# cursor.execute("INSERT INTO Dashboard (date_ca, company_name, ca_name, security_id_type, id_value, ex_date, Rrate, Pay_date, Other, Exception, Remarks) VALUES ('feb2020','jio','dividend','security','id','ex','rec','pay','other',False,'remarks')")

sql = "CREATE TABLE IF NOT EXISTS corporate_actions (id INT AUTO_INCREMENT PRIMARY KEY, company_name VARCHAR(255), type VARCHAR(255), data VARCHAR(5000))"
cursor.execute(sql)

conn.commit() 

# print("Insterted"+ str(cursor.rowcount) + "row into vocab_table")

# cursor.execute("SELECT * FROM Article LIMIT 0")
# fname = cursor.fetchone()[0]
# print(fname)
cursor.execute("SHOW TABLES")
result= cursor.fetchall()
print ('########Created table:',result)

cursor.execute("SELECT * FROM Articles")
articles = cursor.fetchall()
print(articles)
cursor.execute("SELECT * FROM Pages")
Pages = cursor.fetchall()
print(Pages)
cursor.execute("SELECT * FROM Websites")
Websites = cursor.fetchall()
print(Websites)
cursor.execute("SELECT * FROM Company")
Company = cursor.fetchall()
print(Company)
cursor.execute("SELECT * FROM Table_1")
Table_1 = cursor.fetchall()
print(Table_1)
cursor.execute("SELECT * FROM Securities")
Securities = cursor.fetchall()
print(Securities)
cursor.execute("SELECT * FROM Dashboard")
Dashboard = cursor.fetchall()
print(Dashboard)
cursor.execute("SELECT * FROM corporate_actions")
corporate_actions = cursor.fetchall()
print(corporate_actions)

# sql = "CREATE TABLE Pages (page_id int NOT NULL,page_url VARCHAR(30),page_keywords VARCHAR(30),page_old_rank int NOT NULL,
#     page_new_rank int NOT NULL,
#     FOREIGN KEY (page_id) REFERENCES Articles(article_Id)
# )"
# cursor.execute(sql)