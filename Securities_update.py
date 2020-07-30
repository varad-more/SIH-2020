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
# def securities_update(Company_name):
    
    try:
      
        # sql_update_query = ("INSERT INTO Company_name = %s,Security_type = %s,ISIN = %s,Trade_volume = %d,Listed_on_exchange = %s,Exchange_symbol = %s"
        sql_update_query = ("INSERT INTO Securities(Company_name,Security_type,ISIN,Trade_volume,Listed_on_exchange,Exchange_symbol) VALUES(%s,%s,%s,%s,%s,%s)")

        inputData = (Company_name,Security_type,ISIN,Trade_volume,Listed_on_exchange,Exchange_symbol)
        # inputData = (Company_name,None,None,None,None,None)

        cursor.execute(sql_update_query, inputData)
        conn.commit()
        print("Record Updated successfully ")

    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))
    

# securities_update('e','f','yyy', '2' ,'h','d')

securities_update(Company_name,Security_type,ISIN,Trade_volume,Listed_on_exchange,Exchange_symbol)
# conn.commit()
print("Record Updated successfully ")


cursor.execute("SELECT * FROM Securities")
Securities = cursor.fetchall()
print(Securities)

conn.commit()
# finally:
#     if (conn.is_connected()):
#         cursor.close()
#         conn.close()
#         print("MySQL connection is closed")


