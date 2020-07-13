import scrapy 
from scrapy.loader import ItemLoader
from next_gen.items import NextGenItem


class spider1(scrapy.Spider):
    name = "spider1"

    start_urls = [
        "http://web.ist.utl.pt/~luis.tarrataca/classes/computer_architecture/"
    ]
    # c = response.xpath("//following::tr[4]/td[2]/a[contains(@href,'.pdf')]")

    def parse (self, response):
        for link in response.xpath("//following::tr[4]/td[2]/a[@href]"):
            loader = ItemLoader(item = NextGenItem(),selector=link)
            relative_url = link.xpath(".//@href").extract_first()
            absolute_url = response.urljoin(relative_url)
            loader.add_value('file_urls', absolute_url)
            yield loader.load_item()