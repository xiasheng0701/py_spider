import random
import threading
import time
from concurrent import futures
import re

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2306.400 QQBrowser/9.5.10530.400'}
# 检测代理ip有效性的网站
CHECK_URL = 'https://www.baidu.com'
# 获取数目
NUM = 9999
# 调用api(西刺代理)
FETCH_URL = 'http://www.89ip.cn/tqdl.html?api=1&num='+str(NUM)+'&port=&address=&isp='
# 有效代理ip列表
proxies = []
# 代理类型（http/https）
PROXY_TYPE = 'https'
# 线程池，用于同时验证多个代理ip
POOL = futures.ThreadPoolExecutor(max_workers=50)


def add_proxy(proxy: str):
    """
    添加代理
    :param proxy: 代理ip+端口号
    :return:
    """
    try:
        r = requests.get(CHECK_URL, proxies={PROXY_TYPE: proxy}, timeout=30)
        if r.status_code == 200:
            print('有效代理：', proxy)
            # 将有效代理写入文件
            with open('./IP_LIST.txt', 'a', encoding='utf-8') as f:
                f.write(proxy+"\n")
    except Exception as e:
        proxies.remove(proxy)
        print(e)


def fetch_proxy(proxies):
    """
    抓取代理ip
    :return:
    """
    if len(proxies) < 2000:
        req = requests.get(FETCH_URL)
        text = re.findall('\n</script>\n([\s\S]*?)<br><br>', req.text)[0]
        proxies = text.split("<br>")
    for proxy in proxies:
        POOL.submit(add_proxy, proxy)


def run():
    try:
        fetch_proxy(proxies)
    except Exception as e:
        print(e)


# 启动抓取线程
threading.Thread(target=run).start()