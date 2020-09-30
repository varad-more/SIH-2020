#SCRIPT FOR AISHWARYA TO UPDATE THE SECURITIES TABLE:


import mysql.connector
from mysql.connector import Error
Date_ca = 'July'
Company_name = 'Jio'
CA_name = 'Dividend'
Security_id_type = 'Security'
Id_value = 'ID'
Ex_date = 'Ex'
Rec_date = 'Rec'
Pay_date = 'Pay'
Other = 'Other'
Exception = 0
Remarks = 'Remarks'

conn = mysql.connector.connect(host='localhost',
                                    database='fis_2',
                                    user='root',
                                    password='')
cursor = conn.cursor()


def dashboard_update(Date_ca,Company_name,CA_name,Security_id_type,Id_value,Ex_date,Rec_date,Pay_date,Other,Exception,Remarks):

    
    try:
      
        sql_update_query = ("INSERT INTO Securities(Date_ca,Company_name,CA_name,Security_id_type,Id_value,Ex_date,Rec_date,Pay_date,Other,Exception,Remarks) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

        inputData = (Date_ca,Company_name,CA_name,Security_id_type,Id_value,Ex_date,Rec_date,Pay_date,Other,Exception,Remarks)
        # inputData = (Company_name,None,None,None,None,None)

        cursor.execute(sql_update_query, inputData)
        conn.commit()
        print("Record Updated successfully ")

    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))
    



dashboard_update(Date_ca,Company_name,CA_name,Security_id_type,Id_value,Ex_date,Rec_date,Pay_date,Other,Exception,Remarks)

print("Record Updated successfully ")


cursor.execute("SELECT * FROM Dashboard")
Dashboard = cursor.fetchall()
print(Dashboard)

conn.commit()


