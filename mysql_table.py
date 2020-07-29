import mysql.connector
import re
from mysql.connector import Error

try:
    conn = mysql.connector.connect(host='localhost',
                                         database='fis_2',
                                         user='root',
                                         password='')
    if conn.is_connected():
        db_Info = conn.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchall()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
# finally:
#     if (connection.is_connected()):
#         cursor.close()
#         connection.close()
#         print("MySQL connection is closed")
# conn = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     password = "",
#     database = "fis_2"
# )

cursor = conn.cursor()

found = False

for db in cursor:
    pattern = "[(,')]"
    db_string = re.sub(pattern,"", str(db))
    if(db_string == 'fis_2'):
        found = True
        print("database fis_2 exists")
        cursor.execute("use fis_2")

    if(not found):
        cursor.execute("CREATE database fis_2")
        cursor.execute("use fis_2")


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
sql = "CREATE TABLE IF NOT EXISTS Articles (Article_Id int NOT NULL,Article_url VARCHAR(30),Article_title VARCHAR(30),   Article_keywords VARCHAR(30),Article_content VARCHAR(30),Article_author VARCHAR(30),Article_old_rank int NOT NULL,Article_new_rank int NOT NULL,Article_error VARCHAR(5),Article_verified BOOLEAN NULL)"
cursor.execute(sql)

# cursor.execute("INSERT INTO Articles (Article_Id, Article_url, Article_title, Article_keywords, Article_content, Article_author, Article_old_rank, Article_new_rank, Article_error) VALUES('1','url','title','keywords','content','author','2','4','error')")

##Pages
sql = "CREATE TABLE IF NOT EXISTS Pages (Page_Id int NOT NULL,Page_url VARCHAR(30),Page_keywords VARCHAR(30),Page_old_rank int NOT NULL,Page_new_rank int NOT NULL)"
cursor.execute(sql)

# cursor.execute("INSERT INTO Pages (Page_Id ,Page_url, Page_keywords, Page_old_rank, Page_new_rank) VALUES ('1','url','keywords','2','4')")

##Websites
sql = "CREATE TABLE IF NOT EXISTS Websites (Web_Id int NOT NULL,Web_url VARCHAR(30),Web_old_rank int NOT NULL,Web_new_rank int NOT NULL)"
cursor.execute(sql)

# cursor.execute("INSERT INTO Websites (Web_Id, Web_url, Web_old_rank, Web_new_rank) VALUES ('1','url','2','4')")

##Company
sql = "CREATE TABLE IF NOT EXISTS Company (Company_name TEXT NULL,Securities_ex VARCHAR(10),Company_web_link VARCHAR(30),Op_timeline VARCHAR(10),Trading_location VARCHAR(10))"
cursor.execute(sql)

# cursor.execute("INSERT INTO Company (Company_name, Securities_ex, Company_web_link, Op_timeline, Trading_location) VALUES ('Jio','a','b','c','d')")

##Securities
sql = "CREATE TABLE IF NOT EXISTS Securities (Company_name TEXT NULL,Security_type VARCHAR(10),ISIN VARCHAR(10),Trade_volume TEXT NOT NULL,Listed_on_exchange VARCHAR(20),Exchange_symbol VARCHAR(10))"
cursor.execute(sql)

# cursor.execute("INSERT INTO Securities (Security_type,ISIN, Trade_volume,Listed_on_exchange,Exchange_symbol) VALUES ('e','f','1','g','h')")

##Table_1
sql = "CREATE TABLE IF NOT EXISTS Table_1 (Company_name TEXT NULL,Parent_link VARCHAR(20),file_url VARCHAR(20),publish_date VARCHAR(5))"
cursor.execute(sql)

# cursor.execute("INSERT INTO Table_1 (Parent_link,file_url,publish_date) VALUES ('e','f','1')")

##Dashboard
sql = "CREATE TABLE IF NOT EXISTS Dashboard (Date_ca TEXT NULL,Company_name TEXT NULL,CA_name TEXT NULL,Security_id_type TEXT NULL,Id_value TEXT NULL,Ex_date TEXT NULL,Rec_date TEXT NULL,Pay_date TEXT NULL, Other VARCHAR(30),Exception BOOLEAN NULL,Remarks VARCHAR(10))"
cursor.execute(sql)

# cursor.execute("INSERT INTO Dashboard (Date_ca, Company_name, CA_name, Security_id_type, Id_value, Ex_date, Rec_date, Pay_date, Other, Exception, Remarks) VALUES ('feb2020','jio','dividend','security','id','ex','rec','pay','other',False,'remarks')")

sql = "CREATE TABLE IF NOT EXISTS corporate_actions (id INT AUTO_INCREMENT PRIMARY KEY, company_name VARCHAR(255), type VARCHAR(255), data VARCHAR(5000))"
cursor.execute(sql)

conn.commit() 

# print("Insterted"+ str(cursor.rowcount) + "row into vocab_table")

# cursor.execute("SELECT * FROM Article LIMIT 0")
# fname = cursor.fetchone()[0]
# print(fname)
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

# sql = "CREATE TABLE Pages (Page_Id int NOT NULL,Page_url VARCHAR(30),Page_keywords VARCHAR(30),Page_old_rank int NOT NULL,
#     Page_new_rank int NOT NULL,
#     FOREIGN KEY (Page_Id) REFERENCES Articles(Article_Id)
# )"
# cursor.execute(sql)