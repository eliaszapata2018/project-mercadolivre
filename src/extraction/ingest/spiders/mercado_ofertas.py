import scrapy


class MercadoOfertasSpider(scrapy.Spider):
    name = "mercado_ofertas"
    allowed_domains = ["www.mercadolivre.com.br"]
    start_urls = ["https://www.mercadolivre.com.br/ofertas"]
    page_count = 1
    max_page = 10

    def parse(self, response):
        products = response.css('div.andes-card.poly-card.poly-card--grid-card.andes-card--flat.andes-card--padding-0.andes-card--animated')

        for product in products:
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            product_link = product.css('a.poly-component__title::attr(href)').get()

            item = {
                'brand': product.css('span.poly-component__brand::text').get(),
                'name': product.css('a.poly-component__title::text').get(),
                'seller': product.css('span.poly-component__seller::text').get(),
                'reviews_rating_number': product.css('span.poly-reviews__rating::text').get(),
                'reviews_amount': product.css('span.poly-reviews__total::text').get(),
                'old_money': prices[0] if len(prices) > 0 else None,
                'new_money': prices[1] if len(prices) > 1 else None,
                'product_link': product_link  # puedes guardarlo si lo necesitas luego
            }

            if product_link:
                yield response.follow(
                    url=product_link,
                    callback=self.parse_detail,
                    meta={'item': item}
                )

        # paginación
        if self.page_count < self.max_page:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield response.follow(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']

        # Extraer todas las categorías del breadcrumb
        categories = response.css('ol.andes-breadcrumb li a::text').getall()

        # Puedes quedarte con la última (más específica) o toda la lista
        # item['category'] = categories[-1] if categories else None
        item['category_path'] = " > ".join(categories) if categories else None  # opcional, para ver toda la jerarquía

        yield item

