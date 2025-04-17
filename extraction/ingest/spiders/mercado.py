import scrapy


class MercadoSpider(scrapy.Spider):
    name = "mercado"
    allowed_domains = ["www.mercadolivre.com.br"]
    start_urls = ["https://www.mercadolivre.com.br/"]

    def parse(self, response):
        pass
