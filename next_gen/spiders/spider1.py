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
        # yield scrapy.Request('https://www.ril.com/InvestorRelations/Corporate-Announcements.aspx', self.parse)
        # yield scrapy.Request('https://www.silvertouch.com/about-us/investors/', self.parse)
        # yield scrapy.Request('https://www.tcs.com/view-all-corporate-actions#searchIn=/content/tcs/_en&tagId=tcs_discover-tcs/investor-relations/ir-corporate-actions&sortBy=publishedDate&M=yes&Y=yes&IR=true', self.parse)
        yield scrapy.Request('https://www.dabur.com/in/en-us/investor/investor-information/notices/record-date-book-closure', self.parse)
        # yield scrapy.Request('https://www.nestle.in/media/specialannouncements', self.parse)
        yield scrapy.Request('https://www.dabur.com/in/en-us/investor/investor-information/notices/board-meetings', self.parse)
        # yield scrapy.Request('https://www.godrejagrovet.com/corporate-announcements.aspx', self.parse)
        yield scrapy.Request('https://www.dabur.com/in/en-us/investor/investor-information/notices/annual-general-meetings', self.parse) 
        yield scrapy.Request('https://www.dabur.com/in/en-us/investor/investor-information/notices/notices-of-agm-postal-ballots', self.parse)  
        
        

    def parse(self, response):
        # link = response.xpath("//a")
        # print(link)
        
        # mydatabase = mysql.connector.connect (host = 'localhost', user = 'root',password='', database = 'temp_sih')
        # mycursor = mydatabase.cursor()
        
        mydatabase = mysql.connector.connect (host='database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com', user='admin', password='SIH_2020',database='web_server')
        mycursor = mydatabase.cursor()

        print (mycursor)
        link = response.xpath("//@href").extract()
        print (type(response.url))
        for abs_urls in link:
            if (abs_urls[-4:] == '.pdf'):
                loader = ItemLoader(item = NextGenItem(),selector=link)
                absolute_url = response.urljoin(abs_urls)
                str_absolute_url = str(absolute_url)
                #print (absolute_url)
                temp_filename = abs_urls.split('/')
                # final_filename = ''
                for i in temp_filename:
                    if (i[-4:] == '.pdf'):
                        loader.add_value('file_name',i)
                        # final_filename = str(i)
                        # print (i)        
                
                parent_link = response.url
                company_name_temp = parent_link.split('/')
                company_name = ''
                for i in company_name_temp:
                    if ((i[-4:] == '.com') | (i[-4:] == '.in')):
                        company_name = i


                query_search_1 = ("select count(id) from dashboard_file_download")
                mycursor.execute(query_search_1)                
                result_1 = mycursor.fetchall()
                print (result_1[0][0])

                if (result_1[0][0] != 0):
                    query_search = ("select id from dashboard_file_download where url_of_file = (%s)")
                    query_value = (str(absolute_url))
                    mycursor.execute(query_search,(query_value,))
                    result = mycursor.fetchall()
                 
                    file_hash_temp =  hashlib.sha1(str_absolute_url.encode())
                    file_hash = file_hash_temp.hexdigest()
                    if (len(result) == 0 ):
                        values = (company_name, parent_link ,str(absolute_url),file_hash)
                        query_insert = "INSERT INTO dashboard_file_download (company_name, parent_link,url_of_file,sha_file)  values (%s,%s,%s,%s)"
                        mycursor.execute (query_insert, values)
                        mydatabase.commit()
                        loader.add_value('file_urls', absolute_url)
                        yield loader.load_item()
                else:
                    file_hash_temp =  hashlib.sha1(str_absolute_url.encode())
                    file_hash = file_hash_temp.hexdigest()
                    values = (company_name, parent_link ,str(absolute_url),file_hash)
                    query_insert = "INSERT INTO dashboard_file_download (company_name, parent_link,url_of_file,sha_file)  values (%s,%s,%s,%s)"
                    mycursor.execute (query_insert, values)
                    mydatabase.commit()
                    loader.add_value('file_urls', absolute_url)
                    yield loader.load_item()

