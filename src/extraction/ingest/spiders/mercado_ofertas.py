import scrapy


class MercadoOfertasSpider(scrapy.Spider):
    name = "mercado_ofertas"
    allowed_domains = ["www.mercadolivre.com.br"]
    start_urls = ["https://www.mercadolivre.com.br/ofertas#c_id=/home/promotions-recommendations"]

    def parse(self, response):
        pass
#span.poly-component__brand