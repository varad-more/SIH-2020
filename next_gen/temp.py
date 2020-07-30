import mysql.connector as sql

'''
#localhost 
mydatabase = sql.connect (host = 'localhost', user = 'root', database = 'temp_sih')
print (mydatabase)
'''


#aws 
myrds =  sql.connect (host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com', user='admin', password='SIH_2020',database='innodb')
mycursor = myrds.cursor()
print (myrds)
