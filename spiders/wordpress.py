import scrapy
import json
from django.utils.html import strip_tags
# scrapy crawl wordpress_news -o news24nepal.csv -t csv
# scrapy crawl wordpress_news -o nepalitribune.csv -t csv
# curl http://demo.wp-api.org/wp-json/wp/v2/posts
# scrapy crawl news_pahilo -o file.csv -t csv
# ["https://www.news24nepal.tv/", "https://nepalitribune.com/", 'https://www.nepalitimes.com/']
# https://hamrakura.com   nav > ul > li:last-child > a
# https://hamrakura.com/category.php?_Id=1&p=9

class wordpressSpider(scrapy.Spider):
    name = "wordpress_news"
    domain = "https://nepalitribune.com/"
    categories = {}
    total_news = 0
    crawled_news = 0
    news_ids = []

    def start_requests(self):
        yield scrapy.Request(url=self.domain+'wp-json/wp/v2/categories?per_page=100', callback=self.get_categories)

    # def set_total_news(self, total):

    def get_post_count(self, response):
        x = response.headers.getlist("x-wp-total")
        print(int(x[0]))
        total = int(x[0])
        # self.set_total_news(int(x[0]))
        # self.get_news(response)
        print("calling set_total_news")
        self.total_news = total
        pages = int(self.total_news/25)+2
        print("total news count {}".format(self.total_news))
        print("total requests {}".format(pages))
        for i in range(1,pages):
            yield scrapy.Request(url=self.domain+'wp-json/wp/v2/posts?per_page=25&page={}'.format(i), callback=self.get_news)


    def get_categories(self, response):
        # yield scrapy.Request(url=self.domain+'http://www.pahilopost.com/archive/{}?year=&month=&day='.format(i), callback=self.parse)
        jsonresponse = json.loads(response.body_as_unicode())

        self.categories
        for cat in jsonresponse:
            self.categories[cat['id']] ={}
            self.categories[cat['id']]['title']= cat['name']
            self.categories[cat['id']]['count']= cat['count']
            self.categories[cat['id']]['crawlled'] = 0
            # self.total_news = self.total_news + cat['count']

        yield scrapy.Request(url=self.domain+'wp-json/wp/v2/posts?per_page=1&page=1', callback=self.get_post_count)
        # 113505
        # self.set_total_news(113505)


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

    # def all_news_fetched():
    #     resp =  True
    #     for key in self.categories.keys():
    #         resp = resp and self.categories[key]['crawlled'] == self.categories[key]['count']
    #     return  resp

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
