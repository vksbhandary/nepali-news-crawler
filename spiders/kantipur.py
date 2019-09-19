import scrapy
import json
from django.utils.html import strip_tags
from datetime import datetime
from django.utils.html import strip_tags
from urllib.parse import urlsplit

from scrapy.selector import Selector
from datetime import datetime, timedelta

'''
Bot logic:
This scraper uses dated links to fetch all the news items.
The website generally has a structure of https://www.kantipurdaily.com/categoryName/todaysDate
This link lets us fetch the news of category categoryName and date todaysDate.
So the scraper start scraping from today's date and stops at start_date as defined at line 46.
'''

class kantiSpider(scrapy.Spider):
    name = "kanti_news"
    domain = "https://www.kantipurdaily.com"
    categories = {
    'news':{'started':False,'error':0,'crawled':0},
    'cricket-world-cup-2019':{'started':False,'error':0,'crawled':0},
    'business':{'started':False,'error':0,'crawled':0},
    'opinion':{'started':False,'error':0,'crawled':0},
    'sports':{'started':False,'error':0,'crawled':0},
    'national':{'started':False,'error':0,'crawled':0},
    'koseli':{'started':False,'error':0,'crawled':0},
    'world':{'started':False,'error':0,'crawled':0},
    'entertainment':{'started':False,'error':0,'crawled':0},
    'blog':{'started':False,'error':0,'crawled':0},
    'diaspora':{'started':False,'error':0,'crawled':0},
    'feature':{'started':False,'error':0,'crawled':0},
    'lifestyle':{'started':False,'error':0,'crawled':0},
    'literature':{'started':False,'error':0,'crawled':0},
    'technology':{'started':False,'error':0,'crawled':0},
    'health':{'started':False,'error':0,'crawled':0},
    'pathakmanch':{'started':False,'error':0,'crawled':0},
    'Interview':{'started':False,'error':0,'crawled':0},
    'Other':{'started':False,'error':0,'crawled':0},
    }
    total_news = 0
    crawled_news = 0
    news_ids = []
    start_date ="2010/01/01"
    headers = {
        'Host': 'www.kantipurdaily.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': "",
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Cookie': '__asc=cd933e9b16bbca000c73e11fe0c; __auc=cd933e9b16bbca000c73e11fe0c; _ga=GA1.2.1437400896.1562237732; _gid=GA1.2.417484617.1562237732; _fbp=fb.1.1562237732623.564077210; _gat=1',
        'TE': 'Trailers',
    }

    def start_requests(self):
        date_str = datetime.strptime(self.start_date, '%Y/%m/%d').strftime('%Y/%m/%d')


        for cat in self.categories.keys():

            yield scrapy.Request(url="{}/{}/{}".format(self.domain,cat,date_str), callback=self.get_categories)

    def get_categories(self, response):
        cat = urlsplit(response.request.url)[2].split("/")[1]
        date = urlsplit(response.request.url)[2].split("/")[2] +"/"+ urlsplit(response.request.url)[2].split("/")[3]+"/"+ urlsplit(response.request.url)[2].split("/")[4]
        news_crawled = 0
        for article in response.css('article'):
                url = article.css("h2 a::attr(href)").extract_first()

                self.categories[cat]["crawled"]+= 1
                news_crawled += 1
                yield scrapy.Request(url="{}{}".format(self.domain,url), callback=self.get_news)

        if datetime.strptime(date, '%Y/%m/%d').date() <= datetime.today().date():
            newdate = datetime.strptime(date, '%Y/%m/%d') + timedelta(days=1)
            newdate= newdate.strftime('%Y/%m/%d')
            yield scrapy.Request(url="{}/{}/{}".format(self.domain,cat,newdate),callback=self.get_categories)


    def get_news(self, response):
        yield {
        'url':  response.request.url ,
        'title': response.css("article div.article-header h1::text").extract_first(),
        'content': strip_tags(response.css("article div.description::text").extract_first()),
        'category': response.css("div.cat_name::text").extract_first(),
        }
