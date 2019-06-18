# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os,time
import urllib.request
from random import choice

IP_LIST = []
for line in open('''IP_LIST.txt'''):
    IP_LIST.append(line.strip())

def get_randip():
    ip = choice(IP_LIST)
    print('ip:%s' % ip)
    return ip


def schedule(a, b, c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('\r%.2f%%' % per, end='')

class WallpapersPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'win4000':
            dir_path = './壁纸/'+item['cla']+'/'+item['name']
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            proxy = urllib.request.ProxyHandler({'https': get_randip()})
            # construct a new opener using your proxy settings
            opener = urllib.request.build_opener(proxy)
            # install the openen on the module-level
            urllib.request.install_opener(opener)
            for i in range(len(item['url'])):
                # make a request
                print('\n%s%d下载中' %(item['name'],i))
                urllib.request.urlretrieve(item['url'][i], dir_path + '/' + item['name'] + str(i)+'.jpg', reporthook=schedule)
        return item
