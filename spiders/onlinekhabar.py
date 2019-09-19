import scrapy
import urllib.parse as urlparse
from django.utils.html import strip_tags

'''
Bot logic:
Simple scrapy bot logic which starts at starting URLS and ends when there are no links to parse.
'''

class onlinekhabar(scrapy.Spider):
    name = "news_onlinekhabar"
    domain = "https://www.kantipurdaily.com"
    categories = {}
    url_cat = {}
    initurls = [
        'https://www.onlinekhabar.com/content/news',
        'https://www.onlinekhabar.com/business',
        'https://www.onlinekhabar.com/content/business/technology',
        'https://www.onlinekhabar.com/content/prabhas-news',
        'https://www.onlinekhabar.com/content/sports-news',
        'https://www.onlinekhabar.com/content/lifestylenews',
        'https://www.onlinekhabar.com/content/ent-news',
        'https://www.onlinekhabar.com/content/bichitra-world',
        'https://www.onlinekhabar.com/content/literature',

    ]
    def start_requests(self):

        for url in self.initurls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        url = response.request.url

        next_url = response.css("a.next.page-numbers::attr(href)").extract_first()
        if next_url:

            yield scrapy.Request(url=next_url, callback=self.parse)

            for article in response.css("div.list__post div.item__wrap"):
                link = article.css("a::attr(href)").extract_first()
                yield scrapy.Request(url=link, callback=self.get_news)


    def get_news(self, response):

        yield{
        'url':  response.request.url,
        'title': response.css("div.nws__title--card h2::text").extract_first(),
        'content': strip_tags(" ".join(response.css("div.details__content div.ok__news--wrap div.main__read--content *::text").getall())),
        'category': response.css("div.custom_breadcrumb > a:nth-last-child(1)::text").extract_first(),
        }
