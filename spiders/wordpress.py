import scrapy
import json
from django.utils.html import strip_tags


'''
Bot logic:
This scraper uses wordpress's REST API to fetch news items. So this scraper logic can be used on any wordpress site if REST APIs are working.
In order to check if a wordpress site can be scraped using this logic.

1. Go to `yourdomainname.com`/wp-json/wp/v2/posts/
2. If you see a bunch of Json data then its good to go
3. If you see 404 error page or forbidden error page then its not supported.
'''

class wordpressSpider(scrapy.Spider):
    name = "wordpress_news"
    domain = "https://nepalitribune.com/"
    categories = {}
    total_news = 0
    crawled_news = 0
    news_ids = []

    def start_requests(self):
        yield scrapy.Request(url=self.domain+'wp-json/wp/v2/categories?per_page=100', callback=self.get_categories)


    def get_post_count(self, response):
        x = response.headers.getlist("x-wp-total")
        print(int(x[0]))
        total = int(x[0])

        print("calling set_total_news")
        self.total_news = total
        pages = int(self.total_news/25)+2
        print("total news count {}".format(self.total_news))
        print("total requests {}".format(pages))
        for i in range(1,pages):
            yield scrapy.Request(url=self.domain+'wp-json/wp/v2/posts?per_page=25&page={}'.format(i), callback=self.get_news)


    def get_categories(self, response):

        jsonresponse = json.loads(response.body_as_unicode())

        self.categories
        for cat in jsonresponse:
            self.categories[cat['id']] ={}
            self.categories[cat['id']]['title']= cat['name']
            self.categories[cat['id']]['count']= cat['count']
            self.categories[cat['id']]['crawlled'] = 0

        yield scrapy.Request(url=self.domain+'wp-json/wp/v2/posts?per_page=1&page=1', callback=self.get_post_count)



    def return_all_cat(self,catids):
        str = ""
        n = 0
        for catid in catids:
            n = n + 1
            str = str + self.categories[catid]['title']
            self.categories[catid]['crawlled'] = self.categories[catid]['crawlled'] + 1
            if not n == len(catids) :
                str = str + " , "

        return str

    def get_news(self, response):
        news_json = json.loads(response.body_as_unicode())
        for news in news_json:
            if not news['id'] in self.news_ids:
                self.crawled_news = self.crawled_news + 1
                self.news_ids.append(news['id'])
                yield {
                'url': news['link'],
                'title': strip_tags(news['title']['rendered']),
                'content': strip_tags(news['content']['rendered']),
                'category': self.return_all_cat(news['categories']),
                }
