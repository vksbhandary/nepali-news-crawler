import scrapy
import urllib.parse as urlparse

# scrapy crawl news_hamrakura -o hamrakura.csv -t csv
# curl http://demo.wp-api.org/wp-json/wp/v2/posts
# scrapy crawl news_pahilo -o file.csv -t csv
# ["https://www.news24nepal.tv/", "https://nepalitribune.com/", 'https://www.nepalitimes.com/']
# https://hamrakura.com   nav > ul > li:last-child > a
# https://hamrakura.com/category.php?_Id=1&p=9
class hamrakura(scrapy.Spider):
    name = "news_hamrakura"
    categories = {}
    url_cat = {}
    def start_requests(self):

        for i in range(1,22):
            yield scrapy.Request(url='https://hamrakura.com/category.php?_Id={}&p=1'.format(i), callback=self.parse)


    def parse(self, response):
        url = response.request.url
        total = int(response.css("div.example.text-center > p > strong::text").extract_first())
        parsed = urlparse.urlparse(url)
        cat =  urlparse.parse_qs(parsed.query)['_Id'][0]
        cat_name = response.css("h1.page-title::text").extract_first()
        page = int(urlparse.parse_qs(parsed.query)['p'][0])
        if page == 1 and total >0:
            t_pages =  int(total/20) +2
            for i in range(2,t_pages):
                yield scrapy.Request(url='https://hamrakura.com/category.php?_Id={}&p={}'.format(cat,i), callback=self.parse)


        for article in response.css("div.catlist  div.same_height div.itemCat"):
            link = article.css("h4 a::attr(href)").extract_first()
            self.categories[link] = cat_name
            yield scrapy.Request(url=link, callback=self.get_news)

    def get_news(self, response):
        # content = ""
        # title = response.css("h1.uk-heading-large::text").extract_first()
        # for article in response.css("div.content *::text").extract():
        #     content = content +" "+article
        yield{
        'url':  response.request.url ,
        'title': response.css("h1.page-title::text").extract_first(),
        'content': " ".join(response.css("div.content-single *::text").getall()),
        'category': self.categories[response.request.url],
        }
