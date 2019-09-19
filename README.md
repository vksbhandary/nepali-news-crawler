# Nepali News crawler

## Installation
In order to use this crawler, just [install](https://docs.scrapy.org/en/latest/intro/install.html) scrapy and clone [this](https://github.com/vksbhandary/nepali-news-crawler/) repository.

```

$ pip3 install scrapy
$ git clone https://github.com/vksbhandary/nepali-news-crawler.git
$ cd nepali-news-crawler
$ scrapy crawl news_hamrakura -o hamrakura.csv -t csv


```

## Supported Sites
1. [hamrakura](https://hamrakura.com/)
1. [kantipurdaily](https://www.kantipurdaily.com)
1. [onlinekhabar](https://www.onlinekhabar.com/)
1. [pahilopost](http://www.pahilopost.com)
1. wordpress website <sup>1</sup>
    - [nepalitribune](https://nepalitribune.com/)
    - [news24nepal](https://www.news24nepal.tv/)
    - [nepalitimes](https://www.nepalitimes.com/)
    - You can use this for any wordpress website <sup>2</sup>
    

## Executing crawler


- Executing [hamrakura](https://hamrakura.com/) crawler
    ```

    $ scrapy crawl news_hamrakura -o hamrakura.csv -t csv

    ```

- Executing [kantipurdaily](https://www.kantipurdaily.com) crawler

    ```

    $ scrapy crawl kanti_news -o kantipur.csv -t csv

    ```

- Executing [onlinekhabar](https://www.onlinekhabar.com/) crawler

    ```

    $ scrapy crawl news_onlinekhabar -o onlinekhabar.csv -t csv

    ```


- Executing [pahilopost](http://www.pahilopost.com) crawler

    ```

    $ scrapy crawl news_pahilo -o file.csv -t csv

    ```
- Executing wordpress crawler

    ```

    $ scrapy crawl wordpress_news -o news24nepal.csv -t csv

    ```



<sup>1</sup> In order to use the wordpress website example you should follow steps:

1. Open file `spiders/wordpress.py`
1. Edit line 14 to add your domain
1. Open your terminal and execute 
    ```$ scrapy crawl wordpress_news -o news24nepal.csv -t csv```
    

<sup>2</sup> In order to check if a wordpress website is supported by this crwaler

1. Go to `yourdomainname.com`/wp-json/wp/v2/posts/
1. If you see a bunch of Json data then its good to go
1. If you see 404 error page or forbidden error page then its not supported.
