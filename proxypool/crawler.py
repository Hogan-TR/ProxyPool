from .config import UserAgent, CRAWL_PAGES, PROXY_TYPE, CHAOS_REDIS_KEY
from .logger import logger
from .db import myredis

from functools import wraps
from lxml import etree
import requests
import random
import time


def send(url):
    """网页请求模块

    Args:
        url: 待请求网址

    Returns:
        1. 结构树化网页
        2. 异常无返回(None)
    """
    headers = {'User-Agent': random.choice(UserAgent)}  # 伪造请求头
    try:
        html = requests.get(url, headers=headers)
        html.raise_for_status()
        return etree.HTML(html.text)
    except Exception:
        logger.error('Fail To Get Proxies', exc_info=True)
        # 异常无返回(None)


class Crawler(object):
    def __init__(self):
        self.redis = myredis
        self.funcs = list()

    def register(self, func):
        self.funcs.append(func)
        @wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        return wrapper

    def run(self):
        for func in self.funcs:
            for proxy in func():
                logger.info("Crawl From %s - %s", func.__name__, proxy)
                self.redis.add(CHAOS_REDIS_KEY, proxy)


crawler = Crawler()


@crawler.register
def crawl_Xila():
    start_url = "http://www.xiladaili.com/gaoni/{}/"

    for page in range(1, CRAWL_PAGES+1):
        html = send(start_url.format(page))

        if html is not None:  # 正确获得返回数据
            for x in range(1, 50 + 1):
                Tpproxy = html.xpath(
                    f"//tbody/tr[{x}]/td[position()<3]/text()")
                if PROXY_TYPE in [proxy.replace('代理', '') for proxy in Tpproxy[1].split(',')]:
                    yield Tpproxy[0]
        time.sleep(random.uniform(1, 3))


@crawler.register
def crawl_Xici():
    start_url = "https://www.xicidaili.com/nn/{}"

    for page in range(1, CRAWL_PAGES+1):
        html = send(start_url.format(page))

        if html is not None:
            for x in range(1, 100+1):
                Tpproxy = html.xpath(
                    f"//tr[@class][{x}]/td[position()=2 or position()=3 or position()=6]/text()")
                if PROXY_TYPE == Tpproxy[2]:
                    proxy = Tpproxy[0] + ':' + Tpproxy[1]
                    yield proxy
        time.sleep(random.uniform(1, 3))


@crawler.register
def crawl_Kuai():
    start_url = "https://www.kuaidaili.com/free/inha/{}/"

    for page in range(1, CRAWL_PAGES+1):
        html = send(start_url.format(page))

        if html is not None:
            for x in range(1, 15+1):
                Tpproxy = html.xpath(
                    f"//tr[{x}]/td[position()=1 or position()=2 or position()=4]/text()")
                if PROXY_TYPE == Tpproxy[2]:
                    proxy = Tpproxy[0] + ':' + Tpproxy[1]
                    yield proxy
        time.sleep(random.uniform(1, 3))


@crawler.register
def crawl_yun():
    start_url = "http://www.ip3366.net/free/?stype=1&page={}"

    for page in range(1, CRAWL_PAGES+1):
        html = send(start_url.format(page))

        if html is not None:
            for x in range(1, 15+1):
                Tpproxy = html.xpath(
                    f"//tr[{x}]/td[position()=1 or position()=2 or position()=4]/text()")
                if PROXY_TYPE == Tpproxy[2]:
                    proxy = Tpproxy[0] + ':' + Tpproxy[1]
                    yield proxy
        time.sleep(random.uniform(1, 3))


@crawler.register
def crawl_66():
    start_url = "http://www.66ip.cn/{}.html"

    for page in range(1, CRAWL_PAGES+1):
        html = send(start_url.format(page))

        if html is not None:
            gData = html.xpath(
                '//tr[position()!=1]/td[position()<3]/text()')
            num = int(len(gData) / 2)
            for _ in range(num):
                yield gData[2*_] + ':' + gData[2*_+1]
        time.sleep(random.uniform(1, 3))


@crawler.register
def crawl_nima():
    start_url = "http://www.nimadaili.com/gaoni/{}/"

    for page in range(1, CRAWL_PAGES+1):
        html = send(start_url.format(page))

        if html is not None:  # 正确获得返回数据
            for x in range(1, 50 + 1):
                Tpproxy = html.xpath(
                    f"//tbody/tr[{x}]/td[position()<3]/text()")
                if PROXY_TYPE in [proxy.replace('代理', '') for proxy in Tpproxy[1].split(',')]:
                    yield Tpproxy[0]
        time.sleep(random.uniform(1, 3))
