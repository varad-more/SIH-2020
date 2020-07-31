import mysql.connector as sql


# #localhost 
# mydatabase = sql.connect (host = 'localhost', user = 'root', database = 'temp_sih')
# print (mydatabase)




#aws_pythanos_connection
myrds =  sql.connect (host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com', user='admin', password='SIH_2020',database='pythanos_main')
mycursor = myrds.cursor()
print (myrds)

#aws_web_server_connection
myrds1 = sql.connect (host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com', user='admin', password='SIH_2020',database='web_server')
mycursor1 = myrds1.cursor()
print (myrds1)


mycursor = myrds.cursor()
query_search = ("select * from corporate_actions ")
mycursor.execute(query_search)
result = mycursor.fetchall()
# print (type(result))
for r in result:
    values = (r[1],r[2],r[3])
    query_insert = "INSERT INTO dashboard_corp_action_data (company_name, ca_type ,data)  values (%s,%s,%s)"
    mycursor1.execute (query_insert, values)
    myrds1.commit()
    # print(type(r[1]))