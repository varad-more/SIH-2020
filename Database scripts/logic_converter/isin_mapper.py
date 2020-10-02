# import csv
# with open('1.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         print(', '.join(row))

# Import pandas 
import pandas as pd 

# reading csv file 
exchange_1 = pd.read_csv("1.csv")
print (len (exchange_1))    

exchange_2 = pd.read_csv("2.csv")
print (exchange_2)

out_df = pd.DataFrame()# columns = []) 
for i in range (0,len(exchange_2)):
    for j in range(0, len(exchange_1)):
        if exchange_2.ISIN[i] == exchange_1.ISIN[j]:
            out_df=out_df.append ({
            "ISIN_1":exchange_2.ISIN[i],
            "ISIN_2": exchange_1.ISIN[j],
            "security_code": int(exchange_2.security_code[i]), 
            "symbol":exchange_1.SYMBOL[j],
            "security_id": exchange_2.Security_Id[i],    
            
            'name_of_company':exchange_1.NAME_OF_COMPANY[j],	 
            'series':exchange_1.SERIES[j],	 
            'date':exchange_1.DATE_OF_LISTING[j],	 
            'paid_up_value':exchange_1.PAID_UP_VALUE[j],	 
            'market_lot':exchange_1.MARKET_LOT[j],
            'face_value': exchange_1.FACE_VALUE[j] ,
            
            # exchange_2.security_code[i],
            'issuer':exchange_2.Issuer_Name[i],	
            # :exchange_2.Security_Id[i],
            'security_name':exchange_2.Security_Name[i],	
            'status':exchange_2.Status[i],
            'group':exchange_2.Group[i],
            'face_value_2':exchange_2.Face_Value[i],	
            'industry':exchange_2.Industry[i],
            'instrument':exchange_2.Instrument[i]          
            }, ignore_index=True)#, exchange_2.Security_Id[i],exchange_1.SYMBOL[j]]], "ISIN":[]}) 
                
        #    exchange_1.SYMBOL,	exchange_1.NAME_OF_COMPANY,	 exchange_1.SERIES,	 exchange_1.DATE_OF_LISTING,	 exchange_1.PAID_UP_VALUE,	 exchange_1.MARKET_LOT	 exchange_1.FACE_VALUE
        #     exchange_2.security_code	exchange_2.Issuer_Name	exchange_2.Security_Id	exchange_2.Security_Name	exchange_2.Status	exchange_2.Group	exchange_2.Face_Value	exchange_2.Industry	exchange_2.Instrument
                
            # mapped_data = [exchange_2.ISIN[i], exchange_1.ISIN[j], exchange_2.security_code[i], exchange_2.Security_Id[i],exchange_1.SYMBOL[j]]
            # out_df.append(mapped_data) # = pd.DataFrame((mapped_data, columns = [])) 
            print (i)


    # print (i)
out_df['face_value'] = out_df['face_value'].astype(int)
out_df['security_code'] = out_df['security_code'].astype(int)
print (out_df)
out_df.to_csv('output.csv')
#Exchange 1:  SYMBOL	NAME_OF_COMPANY	 SERIES	 DATE_OF_LISTING	 PAID_UP_VALUE	 MARKET_LOT	ISIN	 FACE_VALUE
#Exchange 2:  security_code	Issuer_Name	Security_Id	Security Name	Status	Group	Face_Value	ISIN	Industry	Instrument
