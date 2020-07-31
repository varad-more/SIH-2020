#SCRIPT FOR SURAJ TO EXTRACT CONTENT KEYWORDS WHERE VALUE IN VERIFIED COLUMN IS NULL AND UPDATE IT with TRUE/FALSE
import time
s = time.time()
import mysql.connector
from mysql.connector import Error

def verify_article(Article_verified,Article_Id, Article_keywords,Article_content ,Article_old_rank, Article_new_rank):
    try:
        conn = mysql.connector.connect(host='localhost',
                                             database='fis_2',
                                             user='root',
                                             password='')

        cursor = conn.cursor()

        sql = "SELECT Article_keywords, Article_content, Article_old_rank, Article_new_rank, Article_Id FROM Articles WHERE Article_verified IS NULL"
        cursor.execute(sql)
        Article_content = cursor.fetchone()
    
        print(Article_old_rank)

        conn.commit()

        sql_update_query = """Update Articles set Article_verified = %s where Article_Id = %s"""
        inputData = (verified_status,Article_Id)
        cursor.execute(sql_update_query, inputData)
        conn.commit()
        print("Record Updated successfully ")




    except mysql.connector.Error as error:
        print("Failed to update record to database: {}".format(error))

print(time.time() - s)

