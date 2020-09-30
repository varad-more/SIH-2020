import mysql.connector

# pip3 install mysql-connector-python 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="corporate_actions" # Change as per requirements
)

mycursor = mydb.cursor()

#Reading from Database
mycursor.execute("SELECT * FROM company_list")
rows = mycursor.fetchall()
print (rows)


#Inserting into Database
sql = ("INSERT INTO company_list (id, company_name, location ) values (%s, %s, %s)") 
data = ("2","abc","def")
mycursor.execute(sql, data)
mydb.commit()  # Changes are not commited until you put this, so testing ke liye nikal ke try kar sakte ho.
print(mycursor.rowcount, "record inserted.")

