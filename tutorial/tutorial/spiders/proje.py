import scrapy
import pandas as pd
import matplotlib.pyplot as plt


class Deneme_Spider(scrapy.Spider):
    name = "proje"
    start_urls = [
        "https://www.kitapyurdu.com/index.php?route=product/best_sellers&list_id=1&filter_in_stock=1&filter_in_stock=1&page=1"
    ]
    page_count = 0

    def parse(self, response, **kwargs):
        books_name = response.css("div.name.ellipsis a span::text").extract()
        books_author = response.css("div.author span a span::text").extract()
        books_publisher = response.css("div.publisher span a  span::text").extract()
        kaç_oylama = response.xpath('//*[@class="rating"]/div/@title').extract()
        fiyat = response.xpath('//*[@class="value"]/text()').extract()
        i = 0
        while i < len(books_name):
            yield {
                "KitapAdı": books_name[i],
                "Yazar": books_author[i],
                "Yayıncı": books_publisher[i],
                "KaçKişiOylamış": kaç_oylama[i],
                "fiyat": fiyat[i],
            }
            i += 1
        next_url = response.css("a.next::attr(href)").extract()[0]
        self.page_count += 1
        if next_url is not None and self.page_count != 3:
            yield scrapy.Request(url=next_url, callback=self.parse)

