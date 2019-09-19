import scrapy

'''
Bot logic:
This scraper fetches news from archives. After inspection we have total of 61851 archive items at the time of creation.
This number will always increase as the time processes so please update this number by visiting link http://www.pahilopost.com/archive/?year=&month=&day= .
'''
class pahiloSpider(scrapy.Spider):
    name = "news_pahilo"

    def start_requests(self):
        urls = [
            'http://www.pahilopost.com/archive/?year=&month=&day=',
        ]
        for i in range(14,61851,14):
            yield scrapy.Request(url='http://www.pahilopost.com/archive/{}?year=&month=&day='.format(i), callback=self.parse)


    def parse(self, response):
        for article in response.css("article"):
            url = article.css("h2 a::attr(href)").extract_first()
            yield scrapy.Request(url=url, callback=self.get_news)

    def get_news(self, response):

        yield{
        'title': response.css("h1.uk-heading-large::text").extract_first(),
        'content': " ".join(response.css("div.content *::text").getall()),
        }
