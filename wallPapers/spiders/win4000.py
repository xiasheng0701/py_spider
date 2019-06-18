import scrapy
import re
from wallPapers.items import win4000Item


class NovalSpider(scrapy.Spider):
    name = 'win4000'
    page = 1
    root = 'http://www.win4000.com/wallpaper_191_0_0_1.html'
    allowed_domains = ['win4000.com']
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Referer": root
    }
    def start_requests(self):
        return [scrapy.Request(self.root,headers=self.headers)]
    def parse(self, response):
        cla = response.xpath('''//a[@class='active']/text()''').extract()[0]
        suburl = response.xpath('''//div[@class='list_cont Left_list_cont']/div/div/div/ul/li/a/@href''').extract()
        for url in suburl:
            url = self.get_url(url)
            yield scrapy.Request(url,callback=self.get_item,headers=self.headers,meta = {'cla' : cla})
        try:
            next_page = response.xpath('''//a[@class='next']/@href''').extract()[0]
            yield scrapy.Request(next_page,headers=self.headers)
        except:
            next_page = response.xpath('''//a[@class='active']/following-sibling::a[1]/@href''').extract()[0]
            yield scrapy.Request(next_page, headers=self.headers)
    def get_url(self,url):
        tmp = url.split('_')
        tmp[1]='big'
        str = '_'
        return str.join(tmp)

    def get_item(self, response):
        item = win4000Item()
        piclist = response.xpath('''//div[@class='picBox']/ul/li/a''')
        item['name'] = piclist[0].xpath('''./img/@title''').extract()[0]
        item['url'] = [x.xpath('''./@href''').extract()[0] for x in piclist]
        item['cla'] = response.meta['cla']
        return item
