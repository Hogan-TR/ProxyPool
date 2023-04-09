from .config import UserAgent, CRAWL_PAGES, PROXY_TYPE, CHAOS_REDIS_KEY
from .logger import logger
from .db import myredis

from functools import wraps
from lxml import etree
import requests
import random
import time


class Crawler(object):
    def __init__(self):
        self.redis = myredis
        self.funcs = dict()

    def send(self, url):
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

    def register(self, start_url):
        def decorator(func):
            self.funcs[start_url] = func
            @wraps(func)
            def wrapper(*args, **kw):
                return func(*args, **kw)
            return wrapper
        return decorator

    def run(self):
        for f_url, func in self.funcs.items():
            for page in range(1, CRAWL_PAGES + 1):
                html = self.send(f_url.format(page))
                logger.info("Crawl -> %s: Page %s", func.__name__, page)

                if html is not None:
                    try:
                        for proxy in func(html):
                            logger.info("Crawl From %s - %s",
                                        func.__name__, proxy)
                            self.redis.add(CHAOS_REDIS_KEY, proxy)
                    except Exception:
                        logger.error(
                            'Encountered an error while parsing the web page', exc_info=True)
                time.sleep(random.uniform(1, 3))


crawler = Crawler()


@crawler.register("https://www.kuaidaili.com/free/inha/{}/")
def crawl_Kuai(html):
    for x in range(1, 15+1):
        Tpproxy = html.xpath(
            f"//tr[{x}]/td[position()=1 or position()=2 or position()=4]/text()")
        if PROXY_TYPE == Tpproxy[2]:
            proxy = Tpproxy[0] + ':' + Tpproxy[1]
            yield proxy


# @crawler.register("http://www.xiladaili.com/gaoni/{}/")
# def crawl_Xila(html):
#     for x in range(1, 50 + 1):
#         Tpproxy = html.xpath(
#             f"//tbody/tr[{x}]/td[position()<3]/text()")
#         if PROXY_TYPE in [proxy.replace('代理', '') for proxy in Tpproxy[1].split(',')]:
#             yield Tpproxy[0]


# @crawler.register("http://www.nimadaili.com/gaoni/{}/")
# def crawl_nima(html):
#     for x in range(1, 50 + 1):
#         Tpproxy = html.xpath(
#             f"//tbody/tr[{x}]/td[position()<3]/text()")
#         if PROXY_TYPE in [proxy.replace('代理', '') for proxy in Tpproxy[1].split(',')]:
#             yield Tpproxy[0]


# @crawler.register("https://www.xicidaili.com/nn/{}")
# def crawl_Xici(html):
#     for x in range(1, 100+1):
#         Tpproxy = html.xpath(
#             f"//tr[@class][{x}]/td[position()=2 or position()=3 or position()=6]/text()")
#         if PROXY_TYPE == Tpproxy[2]:
#             proxy = Tpproxy[0] + ':' + Tpproxy[1]
#             yield proxy


# @crawler.register("http://www.ip3366.net/free/?stype=1&page={}")
# def crawl_yun(html):
#     for x in range(1, 15+1):
#         Tpproxy = html.xpath(
#             f"//tr[{x}]/td[position()=1 or position()=2 or position()=4]/text()")
#         if PROXY_TYPE == Tpproxy[2]:
#             proxy = Tpproxy[0] + ':' + Tpproxy[1]
#             yield proxy


# @crawler.register("http://www.66ip.cn/{}.html")
# def crawl_66(html):
#     gData = html.xpath(
#         '//tr[position()!=1]/td[position()<3]/text()')
#     num = int(len(gData) / 2)
#     for _ in range(num):
#         yield gData[2*_] + ':' + gData[2*_+1]
