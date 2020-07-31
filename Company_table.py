#SCRIPT FOR AISHWARYA TO UPDATE THE SECURITIES TABLE:


import mysql.connector
from mysql.connector import Error
Company_name = 'Jio'
Security_type = 'tick'
ISIN = 'something'
Trade_volume = 20
Listed_on_exchange = 'list'
Exchange_symbol = 'Exchange'

conn = mysql.connector.connect(host='localhost',
                                    database='fis_2',
                                    user='root',
                                    password='')
cursor = conn.cursor()


def securities_update(Company_name,Security_type,ISIN,Trade_volume,Listed_on_exchange,Exchange_symbol):

    
    try:
      
        sql_update_query = ("INSERT INTO Securities(Company_name,Security_type,ISIN,Trade_volume,Listed_on_exchange,Exchange_symbol) VALUES(%s,%s,%s,%s,%s,%s)")

        inputData = (Company_name,Security_type,ISIN,Trade_volume,Listed_on_exchange,Exchange_symbol)
        # inputData = (Company_name,None,None,None,None,None)

        cursor.execute(sql_update_query, inputData)
        conn.commit()
        print("Record Updated successfully ")

    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))
    



securities_update(Company_name,Security_type,ISIN,Trade_volume,Listed_on_exchange,Exchange_symbol)

print("Record Updated successfully ")


cursor.execute("SELECT * FROM Securities")
Securities = cursor.fetchall()
print(Securities)

conn.commit()



