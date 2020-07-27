import mysql.connector as sql

mydatabase = sql.connect (host = 'localhost', user = 'root', database = 'temp_sih')
print (mydatabase)


