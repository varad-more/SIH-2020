import scrapy 
from scrapy.loader import ItemLoader
from next_gen.items import NextGenItem
import mysql.connector 
import boto3
import hashlib


class spider1(scrapy.Spider):
    name = "spider1"

    # start_urls = [
    #     "https://www.ril.com/InvestorRelations/Corporate-Announcements.aspx"
    # ]
    # c = response.xpath("//following::tr[4]/td[2]/a[contains(@href,'.pdf')]")
    def start_requests(self):
        yield scrapy.Request('https://www.ril.com/InvestorRelations/Corporate-Announcements.aspx', self.parse)
        yield scrapy.Request('https://www.silvertouch.com/about-us/investors/', self.parse)
        

    def parse(self, response):
        # link = response.xpath("//a")
        # print(link)
        
        # mydatabase = mysql.connector.connect (host = 'localhost', user = 'root',password='', database = 'temp_sih')
        # mycursor = mydatabase.cursor()
        
        mydatabase = mysql.connector.connect (host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com', user='admin', password='SIH_2020',database='pythanos_main',)
        mycursor = mydatabase.cursor()

        print (mycursor)
        link = response.xpath("//@href").extract()
        for abs_urls in link:
            if (abs_urls[-4:] == '.pdf'):
                loader = ItemLoader(item = NextGenItem(),selector=link)
                absolute_url = response.urljoin(abs_urls)
                str_absolute_url = str(absolute_url)
                # print (absolute_url)
                temp_filename = abs_urls.split('/')
                # final_filename = ''
                for i in temp_filename:
                    if (i[-4:] == '.pdf'):
                        loader.add_value('file_name',i)
                        # final_filename = str(i)
                        # print (i)        
                parent_link = "https://www.ril.com/InvestorRelations/Corporate-Announcements.aspx"
                company_name = "ril.com"

                query_search = ("select id from crawler_2 where file_url = (%s)")
                query_value = (str(absolute_url))
                mycursor.execute(query_search,(query_value,))
                result = mycursor.fetchall()
                '''
                query_search = ("select file_url from crawler_2 ")
                mycursor.execute(query_search)
                result = mycursor.fetchall()
                '''


                file_hash_temp =  hashlib.sha1(str_absolute_url.encode())
                file_hash = file_hash_temp.hexdigest()

                # print (len(result))
                if (len(result) == 0 ):
                    values = (company_name, parent_link ,str(absolute_url),file_hash)
                    query_insert = "INSERT INTO crawler_2 (company_name, parent_link,file_url,sha_file)  values (%s,%s,%s,%s)"
                    mycursor.execute (query_insert, values)
                    mydatabase.commit()
                    loader.add_value('file_urls', absolute_url)
                    yield loader.load_item()
                
