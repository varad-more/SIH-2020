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

# sql = "SELECT * FROM vocab_table"

# # value = ('fruit')

# cursor.execute(sql)

# result = cursor.fetchall()
# for row in result:
#     print(row)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# import mysql.connector
# cnxn = mysql.connector.connect(
#     host='localhost',
#         user='root',
#         password='',
#         database='mydb')
# crsr = cnxn.cursor()
# crsr.execute("DROP TABLE IF EXISTS pytest")
# crsr.execute("""
# CREATE TABLE pytest (
#     id INT(11) NOT NULL AUTO_INCREMENT,
#     firstname VARCHAR(20),
#     PRIMARY KEY (id)
#     )
# """)
# crsr.execute("INSERT INTO pytest (firstname) VALUES ('Gord')")
# crsr.execute("INSERT INT
# updateLaptopPrice(7500, 1)
# updateLaptopPrice(5000, 2)ytest (firstname) VALUES ('Anne')")
# cnxn.commit()
# crsr.execute("SELECT firstname FROM pytest LIMIT 0, 1")
# fname = crsr.fetchone()[0]
# print(fname)
# crsr.execute("SELECT firstname FROM pytest")  # OK now

# #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# import mysql.connector

# # pip3 install mysql-connector-python 

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="",
#   database="corporate_actions" # Change as per requirements
# )

# updateLaptopPrice(7500, 1)
# updateLaptopPrice(5000, 2)
# mycursor = mydb.cursor()

# #Reading from Database
# mycursor.execute("SELECT * FROM company_list")
# rows = mycursor.fetchall()
# print (rows)


# updateLaptopPrice(7500, 1)
# updateLaptopPrice(5000, 2)owcount, "record inserted.")

# #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.

# import mysql.connector
# from mysql.connector import Error

# def updateLaptopPrice(id, price):
#     try:
#         connection = mysql.connector.connect(host='localhost',
#                                              database='Electronics',
#                                              user='root',
#                                              password='')

#         cursor = connection.cursor()
#         sql_update_query = """Update Laptop set price = %s where id = %s"""
#         inputData = (price, id)
#         cursor.execute(sql_update_query, inputData)
#         connection.commit()
#         print("Record Updated successfully ")

#     except mysql.connector.Error as error:
#         print("Failed to update record to database: {}".format(error))
#     finally:
#         if (connection.is_connected()):
#             cursor.close()
#             connection.close()
#             print("MySQL connection is closed")


# updateLaptopPrice(7500, 1)
# updateLaptopPrice(5000, 2)