#SCRIPT FOR SURAJ TO CHECK ALL THE NULL VALUES IN VERIFIED
import mysql.connector
import re

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "sih_one"
)

cursor = conn.cursor()
cursor.execute("SHOW DATABASES")
found = False

for db in cursor:
    pattern = "[(,')]"
    db_string = re.sub(pattern,"", str(db))
    if(db_string == 'sih_one'):
        found = True
        print("database sih_one exists")
if(not found):
    cursor.execute("CREATE db sih_one")

sql = "DROP TABLE IF EXISTS vocab_table"
cursor.execute(sql)

sql = "CREATE TABLE vocab_table(word VARCHAR(255), definition VARCHAR(255))"
cursor.execute(sql)

fh = open("vocab_list.csv")

wd_list = fh.readlines()

wd_list.pop(0)

vocab_list = []

for rawstring in wd_list:
    word, definition = rawstring.split(',',1)
    definition = definition.rstrip()
    vocab_list.append({word,definition})
    sql = "INSERT INTO vocab_table(word, definition) VALUES(%s, %s)"
    values = (word,definition)
    cursor.execute(sql, values)
    
    conn.commit()
    print("Insterted"+ str(cursor.rowcount) + "row into vocab_table")