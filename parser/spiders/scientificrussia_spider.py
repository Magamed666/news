import scrapy
import pymysql
from dateparser import parse as dateparse

class ScientificRussiaSpider(scrapy.Spider):
    name = "scientificrussia_spider"

    def __init__(self, source_id, start_url, config, *args, **kwargs):
        super(ScientificRussiaSpider, self).__init__(*args, **kwargs)
        self.source_id = source_id
        self.start_urls = [start_url]
        self.config = config

    def parse(self, response):
        article_links = response.xpath(self.config['article_links']).getall()
        for link in article_links:
            yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        title = response.xpath(self.config['title']).get()
        content = response.xpath(self.config['content']).getall()
        date = response.xpath(self.config['date']).get()

        if title and content:
            news_item = {
                'source_id': self.source_id,
                'link': response.url,
                'title': title,
                'content': ' '.join(content),
                'date': dateparse(date)
            }
            self.save_to_db(news_item)

    def save_to_db(self, item):
        connection = pymysql.connect(host='db', user='root', password='example', database='news_db')
        with connection.cursor() as cursor:
            sql = "INSERT INTO items (source_id, link, title, content, date, created_at) VALUES (%s, %s, %s, %s, %s, NOW())"
            cursor.execute(sql, (item['source_id'], item['link'], item['title'], item['content'], item['date']))
        connection.commit()
        connection.close()
