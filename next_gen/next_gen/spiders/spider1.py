import scrapy 
from scrapy.loader import ItemLoader
from next_gen.items import NextGenItem
import mysql.connector 
import boto3

class spider1(scrapy.Spider):
    name = "spider1"

    start_urls = [
        "https://www.ril.com/InvestorRelations/Corporate-Announcements.aspx"
    ]
    # c = response.xpath("//following::tr[4]/td[2]/a[contains(@href,'.pdf')]")

    def parse(self, response):
        # link = response.xpath("//a")
        # print(link)
        
        mydatabase = mysql.connector.connect (host = 'localhost', user = 'root', database = 'temp_sih')
        mycursor = mydatabase.cursor()
        
        # mydatabase = mysql.connector.connect (host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com', user='admin', password='SIH_2020',database='innodb')
        # mycursor = mydatabase.cursor()

        print (mycursor)

        link = response.xpath("//@href").extract()
        for abs_urls in link:
            if (abs_urls[-4:] == '.pdf'):
                loader = ItemLoader(item = NextGenItem(),selector=link)
                absolute_url = response.urljoin(abs_urls)
                # print (absolute_url)
                temp_filename = abs_urls.split('/')
                final_filename = ''
                for i in temp_filename:
                    if (i[-4:] == '.pdf'):
                        loader.add_value('file_name',i)
                        final_filename = str(i)
                        # print (i)        
                parent_link = "https://www.ril.com/InvestorRelations/Corporate-Announcements.aspx"

                query_search = ("select * from file_download where url_of_file = (%s)")
                query_value = (str(absolute_url))
                mycursor.execute(query_search,(query_value,))
                result = mycursor.fetchall()
                # print (len(result))
                if (len(result) == 0 ):
                    values = (final_filename, parent_link ,str(absolute_url))
                    query_insert = "INSERT INTO file_download values (%s,%s,%s)"
                    mycursor.execute (query_insert, values)
                    mydatabase.commit()
                    loader.add_value('file_urls', absolute_url)
                    yield loader.load_item()
                
