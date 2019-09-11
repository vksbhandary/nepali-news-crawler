import scrapy
import urllib.parse as urlparse
from django.utils.html import strip_tags
# scrapy crawl news_onlinekhabar -o onlinekhabar.csv -t csv
# curl http://demo.wp-api.org/wp-json/wp/v2/posts
# scrapy crawl news_pahilo -o file.csv -t csv
# ["https://www.news24nepal.tv/", "https://nepalitribune.com/", 'https://www.nepalitimes.com/']
# https://hamrakura.com   nav > ul > li:last-child > a
# https://hamrakura.com/category.php?_Id=1&p=9
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
        # tot = response.css("#main > section > div > div > div > div.ok18-pagination-wrap > div > a:nth-last-child(2)::text").extract_first()
        next_url = response.css("a.next.page-numbers::attr(href)").extract_first()
        if next_url:
            # tot = tot.replace(",","")
            # total = int(tot)
            # if "page" not in response.request.url:
            # for i in range(2,total+1):
            yield scrapy.Request(url=next_url, callback=self.parse)

            for article in response.css("div.list__post div.item__wrap"):
                link = article.css("a::attr(href)").extract_first()
                # self.categories[link] = cat_name
                yield scrapy.Request(url=link, callback=self.get_news)
        # else:
        #     print(response.request.url)

    def get_news(self, response):
        # content = ""
        # title = response.css("h1.uk-heading-large::text").extract_first()
        # for article in response.css("div.content *::text").extract():
        #     content = content +" "+article
        yield{
        'url':  response.request.url,
        'title': response.css("div.nws__title--card h2::text").extract_first(),
        'content': strip_tags(" ".join(response.css("div.details__content div.ok__news--wrap div.main__read--content *::text").getall())),
        'category': response.css("div.custom_breadcrumb > a:nth-last-child(1)::text").extract_first(),
        }
