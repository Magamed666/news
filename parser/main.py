import scrapy
from scrapy.crawler import CrawlerProcess
import pymysql
import json

from spiders.nurkz_spider import NurKzSpider
from spiders.tengrinews_spider import TengrinewsSpider
from spiders.scientificrussia_spider import ScientificRussiaSpider

def run_spider(spider, source_id, url, config):
    process = CrawlerProcess()
    process.crawl(spider, source_id=source_id, start_url=url, config=config)
    process.start()

def fetch_tasks():
    connection = pymysql.connect(host='db', user='root', password='example', database='news_db')
    with connection.cursor() as cursor:
        sql = "SELECT id, url, config FROM source"
        cursor.execute(sql)
        tasks = cursor.fetchall()
    connection.close()
    return tasks

if __name__ == "__main__":
    tasks = fetch_tasks()
    for task in tasks:
        source_id, url, config_json = task
        config = json.loads(config_json)
        
        if "nurkz" in url:
            run_spider(NurKzSpider, source_id, url, config)
        elif "tengrinews" in url:
            run_spider(TengrinewsSpider, source_id, url, config)
        elif "scientificrussia" in url:
            run_spider(ScientificRussiaSpider, source_id, url, config)
