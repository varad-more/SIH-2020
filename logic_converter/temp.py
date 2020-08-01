import mysql.connector as sql


# #localhost 
# mydatabase = sql.connect (host = 'localhost', user = 'root', database = 'temp_sih')
# print (mydatabase)




#aws_pythanos_connection
myrds =  sql.connect (host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com', user='admin', password='SIH_2020',database='pythanos_main')
mycursor = myrds.cursor()
print (myrds)

#aws_web_server_connection
# myrds1 = sql.connect (host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com', user='admin', password='SIH_2020',database='web_server')
# mycursor1 = myrds1.cursor()
# print (myrds1)


mycursor = myrds.cursor()

mycursor.execute( """create table security_master (ISIN varchar(12),	date text,	face_value varchar (2),	security_group varchar (1),	industry varchar (20),
	instrument	varchar (10), market_lot varchar(20),	name_of_company varchar (20),	paid_up_value varchar (2),	security_code varchar(6),	security_id varchar (6),
    security_name varchar(50)	, series varchar(2),	symbol varchar (10), nse	boolean,bse boolean, trading_location varchar(5))"""
)
myrds.commit()
# INE208C01025	03-APR-1996	1	A 	Oil Marketing & Distribution	Equity	1	Aegis Logistics Limited	1	500003	AEGISLOG	AEGIS LOGISTICS LTD.	EQ	AEGISCHEM	1	1

query_search = ("select * from security_master ")
mycursor.execute(query_search)
result = mycursor.fetchall()
# print (result)




import pandas as pd 

# reading csv file 
exchange_1 = pd.read_csv("output.csv")
# print (len (exchange_1))
# ISIN	date	face_value	security_group	industry	instrument	market_lot	name_of_company	paid_up_value
# 	security_code	security_id	security_name	series	symbol	nse	bse

exchange_1['ISIN'] = exchange_1 ['ISIN'].astype(str)
exchange_1['date'] = exchange_1 ['date'].astype(str)
exchange_1['security_group'] = exchange_1 ['security_group'].astype(str)
exchange_1['face_value'] = exchange_1 ['face_value'].astype(str)
exchange_1['industry'] = exchange_1 ['industry'].astype(str)
exchange_1['instrument'] = exchange_1 ['instrument'].astype(str)
exchange_1['market_lot'] = exchange_1 ['market_lot'].astype(str)
exchange_1['security_code'] = exchange_1 ['security_code'].astype(str)
exchange_1['paid_up_value'] = exchange_1 ['paid_up_value'].astype(str)
exchange_1['name_of_company'] = exchange_1 ['name_of_company'].astype(str)
exchange_1['security_id'] = exchange_1 ['security_id'].astype(str)
exchange_1['security_name'] = exchange_1 ['security_name'].astype(str)
exchange_1['nse'] = exchange_1 ['nse'].astype(str)
exchange_1['bse'] = exchange_1 ['bse'].astype(str)


# print (exchange_1)
# exchange_1['face_value'] = exchange_1 ['face_value'].astype(int)

# exchange_1['security_code'] = exchange_1['security_code'].astype(float)  
# exchange_1['security_code'] = exchange_1['security_code'].astype(int)  

sql = 'insert into security_master values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
for i in range (0,len(exchange_1)-1):
    # print((exchange_1.iloc[i]))
    # print (len(exchange_1.iloc[i,0]))
    print (i)

    values = (exchange_1.iloc[i,0],exchange_1.iloc[i,1],exchange_1.iloc[i,2],exchange_1.iloc[i,3],exchange_1.iloc[i, 4],exchange_1.iloc[i, 5],exchange_1.iloc[i, 6],exchange_1.iloc[i, 7],exchange_1.iloc[i, 8],exchange_1.iloc[i, 9],exchange_1.iloc[i, 10],exchange_1.iloc[i, 11],exchange_1.iloc[i, 12],exchange_1.iloc[i, 13],exchange_1.iloc[i, 14],exchange_1.iloc[i, 15],exchange_1.iloc[i, 16])
    mycursor.execute(sql,values)


# for r in result:
#     values = (r[1],r[2],r[3])
#     query_insert = "INSERT INTO dashboard_corp_action_data (company_name, ca_type ,data)  values (%s,%s,%s)"
#     mycursor.execute (query_insert, values)
    myrds.commit()
    # print(type(r[1]))

query_search = ("select * from security_master ")
mycursor.execute(query_search)
result = mycursor.fetchall()
print (result)
