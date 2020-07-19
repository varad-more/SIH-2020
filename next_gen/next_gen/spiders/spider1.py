import scrapy 
from scrapy.loader import ItemLoader
from next_gen.items import NextGenItem



class spider1(scrapy.Spider):
    name = "spider1"

    start_urls = [
        "https://www.ril.com/InvestorRelations/Corporate-Announcements.aspx"
    ]
    # c = response.xpath("//following::tr[4]/td[2]/a[contains(@href,'.pdf')]")

    def parse(self, response):
        # link = response.xpath("//a")
        # print(link)
        link = response.xpath("//@href").extract()
        for abs_urls in link:
            if (abs_urls[-4:] == '.pdf'):
                loader = ItemLoader(item = NextGenItem(),selector=link)
                absolute_url = response.urljoin(abs_urls)
                print (absolute_url)
                loader.add_value('file_urls', absolute_url)
                yield loader.load_item()
