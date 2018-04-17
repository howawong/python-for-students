import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

class RTHKSpider(scrapy.Spider):
    name = 'rthk'
    
    def start_requests(self):
        yield scrapy.Request(url='http://www.rthk.hk/', callback=self.process_index_page)
        
    def process_index_page(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        print(soup.title.string)
        items = soup.find('ul', {'class': 'catUl news'})
        links = [item.find('a') for item in items]
        links = [link for link in links if link != -1 and link is not None]
        for link in links:
            print(link['href'])
            yield scrapy.Request(url=link['href'], callback=self.process_detail_page)
            
    def process_detail_page(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        div = soup.find('div', {'class': 'itemFullText'})
        print('=' * 100)
        print(soup.title.string)
        print(div.text)
        print('=' * 100)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'LOG_LEVEL': 'ERROR'
})

process.crawl(RTHKSpider)
process.start() # the script will block here until the crawling is finished