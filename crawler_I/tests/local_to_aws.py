import mysql.connector as sql

#aws_pythanos_connection
aws_rds =  sql.connect (host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com', user='admin', password='SIH_2020',database='pythanos_main')
aws_rds_cursor = aws_rds.cursor()
print (aws_rds)

#aws_web_server_connection
local_db = sql.connect (host='localhost', user='root', password='Abhijit@123',database='deadpan')
local_cursor = local_db.cursor()
print (local_db)


query_search = ("select * from pages where pages_id>21422")#links,webs,pages,errors,
local_cursor.execute(query_search)
result = local_cursor.fetchall()

for r in result:
    values = (r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8])
    query_insert = "INSERT IGNORE INTO pages(pages_id,url,keywords,website,error,old_rank,new_rank,moved,filename)  values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    aws_rds_cursor.execute(query_insert, values)
    aws_rds.commit()
"""

for r in result:
    values = (r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8])
    query_insert = "INSERT INTO pages(pages_id,url,keywords,website,error,old_rank,new_rank,moved,filename)  values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    aws_rds_cursor.execute(query_insert, values)
    aws_rds.commit()


for r in result:
    values = (r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8])
    query_insert = "INSERT INTO pages(pages_id,url,keywords,website,error,old_rank,new_rank,moved,filename)  values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    aws_rds_cursor.execute(query_insert, values)
    aws_rds.commit()


for r in result:
    values = (r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8])
    query_insert = "INSERT INTO pages(pages_id,url,keywords,website,error,old_rank,new_rank,moved,filename)  values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    aws_rds_cursor.execute(query_insert, values)
    aws_rds.commit()


for r in result:
    values = (r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8])
    query_insert = "INSERT INTO pages(pages_id,url,keywords,website,error,old_rank,new_rank,moved,filename)  values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    aws_rds_cursor.execute(query_insert, values)
    aws_rds.commit()

"""
# aws_rds_cursor.execute("TRUNCATE TABLE webs,pages,links,errors")
# aws_rds.commit()