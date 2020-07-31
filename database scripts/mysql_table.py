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
        cursor.execute("create database pythanos_main;")
        # cursor.execute('create database web_server;')
        cursor.execute("show databases")
        res = cursor.fetchall()
        print("Available databases: ", res)

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    cursor.close()

try:
    conn = mysql.connector.connect(host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com',
                                         database='pythanos_main',
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
sql = """CREATE TABLE IF NOT EXISTS articles
                                    (
                                        id INT PRIMARY KEY auto_increment,
                                        url varchar(1000) UNIQUE,
                                        company_name varchar(500),
                                        error INT,
                                        authors varchar(1000),
                                        publish_date varchar(1000),
                                        title varchar(1000),
                                        content varchar(10000),
                                        keywords varchar(5000), 
                                        filename varchar(5000),
                                        rank FLOAT
                                    );"""

cursor.execute(sql)

sql = """ALTER TABLE articles CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"""
cursor.execute(sql)


##links
sql = """CREATE TABLE IF NOT EXISTS links
                                    (
                                     from_id INT,
                                        to_id INT,
                                        UNIQUE(from_id, to_id)
                                    );"""
cursor.execute(sql)

##webs
sql = """CREATE TABLE IF NOT EXISTS webs
                                    (   name varchar(100),
                                        url varchar(1000) UNIQUE,
                                        web_rank FLOAT
                                    );"""
cursor.execute(sql)


##errors
sql = """CREATE TABLE IF NOT EXISTS errors
                                    (
                                        url varchar(1000) UNIQUE,
                                        exception varchar(2000)
                                    );"""

cursor.execute(sql)


##pages
sql = """CREATE TABLE IF NOT EXISTS pages 
        (pages_id INT PRIMARY KEY auto_increment,
         url varchar(1000) UNIQUE, 
         keywords varchar(5000), 
         website varchar(5000), 
         error INT, 
         old_rank FLOAT, 
         new_rank FLOAT, 
         moved INT, 
         filename varchar(500));"""

cursor.execute(sql)

# cursor.execute("INSERT INTO Pages (page_id ,page_url, page_keywords, page_old_rank, page_new_rank) VALUES ('1','url','keywords','2','4')")

##websites
sql = """CREATE TABLE IF NOT EXISTS websites
        (web_id int NOT NULL, 
        web_url VARCHAR(100), 
        web_old_rank int NOT NULL, 
        web_new_rank int NOT NULL);"""

cursor.execute(sql)

# cursor.execute("INSERT INTO Websites (web_id, web_url, web_old_rank, web_new_rank) VALUES ('1','url','2','4')")

##Company
sql = """CREATE TABLE IF NOT EXISTS company 
        (company_name TEXT NULL,
        securities_ex VARCHAR(10),
        company_web_link VARCHAR(30),
        op_timeline VARCHAR(10),
        trading_location VARCHAR(10));"""

cursor.execute(sql)

# cursor.execute("INSERT INTO Company (company_name, securities_ex, company_web_link, op_timeline, trading_location) VALUES ('Jio','a','b','c','d')")

##securities
sql = """CREATE TABLE IF NOT EXISTS securities 
        ( id int NOT NULL,company_name TEXT NULL,
        security_type VARCHAR(100),
        isin VARCHAR(20),
        trade_volume TEXT NOT NULL,
        listed_on_exchange VARCHAR(20),
        exchange_symbol VARCHAR(100),
        PRIMARY KEY (id), 
        FOREIGN KEY (id) REFERENCES articles(id));"""

cursor.execute(sql)

# cursor.execute("INSERT INTO Securities (security_type,ISIN, trade_volume,listed_on_exchange,Exchange_symbol) VALUES ('e','f','1','g','h')")

##crawler_2
sql = """CREATE TABLE IF NOT EXISTS crawler_2 
        (id  int AUTO_INCREMENT PRIMARY KEY, 
        company_name varchar (100) NULL
        ,parent_link VARCHAR(250),
        file_url VARCHAR(250), 
        sha_file varchar(200));"""

# publish date removal and varchar 300.
cursor.execute(sql)


##dashboard
sql = """CREATE TABLE IF NOT EXISTS dashboard 
        (date_ca TEXT NULL,
        company_name TEXT NULL,
        ca_name TEXT NULL,
        security_id_type TEXT NULL,
        id_value TEXT NULL,
        ex_date TEXT NULL,
        rec_date TEXT NULL,
        pay_date TEXT NULL, 
        other VARCHAR(30),
        exception BOOLEAN NULL,
        remarks VARCHAR(10));"""

cursor.execute(sql)

# cursor.execute("INSERT INTO Dashboard (date_ca, company_name, ca_name, security_id_type, id_value, ex_date, Rrate, Pay_date, Other, Exception, Remarks) VALUES ('feb2020','jio','dividend','security','id','ex','rec','pay','other',False,'remarks')")

sql = """CREATE TABLE IF NOT EXISTS historic_data 
        (id INT AUTO_INCREMENT PRIMARY KEY, 
        company_name VARCHAR(255), 
        type VARCHAR(255), 
        data VARCHAR(5000));"""

cursor.execute(sql)

conn.commit() 


cursor.execute("SHOW TABLES")
result= cursor.fetchall()
print ('----------------------Created table:-------------------',result)

cursor.execute("SELECT * FROM articles")
articles = cursor.fetchall()
print(articles)
cursor.execute("SELECT * FROM pages")
Pages = cursor.fetchall()
print(Pages)
cursor.execute("SELECT * FROM webs")
Websites = cursor.fetchall()
print(Websites)
cursor.execute("SELECT * FROM company")
Company = cursor.fetchall()
print(Company)
cursor.execute("SELECT * FROM crawler_2")
Table_1 = cursor.fetchall()
print(Table_1)
cursor.execute("SELECT * FROM securities")
Securities = cursor.fetchall()
print(Securities)
cursor.execute("SELECT * FROM dashboard")
Dashboard = cursor.fetchall()
print(Dashboard)
