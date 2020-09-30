#SCRIPT FOR PRATHAMESH TO UPDATE TABLE_1:


import mysql.connector
from mysql.connector import Error

Company_name = 'Jio'
Parent_link = 'jio.com'
file_url = 'www.blablabla.com'
publish_date = 'June 2020'

conn = mysql.connector.connect(host='localhost',
                                    database='fis_2',
                                    user='root',
                                    password='')
cursor = conn.cursor()


def table_1_update(Company_name,Parent_link,file_url,publish_date):

    
    try:
      
        sql_update_query = ("INSERT INTO Securities(Company_name,Parent_link,file_url,publish_date) VALUES(%s,%s,%s,%s)")

        inputData = (Company_name,Parent_link,file_url,publish_date)
        # inputData = (Company_name,None,None,None,None,None)

        cursor.execute(sql_update_query, inputData)
        conn.commit()
        print("Record Updated successfully ")

    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))
    



table_1_update(Company_name,Parent_link,file_url,publish_date)

print("Record Updated successfully ")


cursor.execute("SELECT * FROM Table_1")
Table_1 = cursor.fetchall()
print(Table_1)

conn.commit()


