import scrapy
# scrapy crawl <spider name> -o file.csv -t csv
# curl http://demo.wp-api.org/wp-json/wp/v2/posts
# scrapy crawl news_pahilo -o file.csv -t csv
# ["https://www.news24nepal.tv/", "https://nepalitribune.com/", 'https://www.nepalitimes.com/']
# https://hamrakura.com   nav > ul > li:last-child > a
# https://hamrakura.com/category.php?_Id=1&p=9
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
        # content = ""
        # title = response.css("h1.uk-heading-large::text").extract_first()
        # for article in response.css("div.content *::text").extract():
        #     content = content +" "+article
        yield{
        'title': response.css("h1.uk-heading-large::text").extract_first(),
        'content': " ".join(response.css("div.content *::text").getall()),
        }
