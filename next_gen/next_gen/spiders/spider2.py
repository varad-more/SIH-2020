import scrapy 
from scrapy.loader import ItemLoader
from next_gen.items import NextGenItem
import mysql.connector 
import boto3

class spider2(scrapy.Spider):
    name = "spider2"

    start_urls = ["https://www.silvertouch.com"
    # ,"https://www.tatamotors.com/"
    ]

    def parse (self, response):
        '''
        check in the database if the link for CA is present or not 
        else find the link
        '''

        '''
        to find the link
        '''
        links = response.xpath("//@href").extract()

        target_link = []
        for link in links:
            if (link.find("investors")>0) | ((link.find("corporate")>0)) :
                target_link.append(link)
            else:
                pass
        print (target_link)

