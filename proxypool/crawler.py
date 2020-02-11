from .config import UserAgent, CRAWL_PAGES, PROXY_TYPE, CHAOS_REDIS_KEY
from .logger import logger
from .db import myredis

from lxml import etree
import requests
import random
import time


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        #:cls: 当前准备创建的类的对象
        #:name: 类的名字
        #:bases: 类继承的父类集合
        #:attrs: 类的方法集合

        count = 0
        attrs['__CrawlFunc__'] = list()
        for kname in attrs.keys():
            if 'crawl_' in kname:
                attrs['__CrawlFunc__'].append(kname)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def __init__(self):
        self.redis = myredis

    def run(self):
        proxies = list()  # 代理信息暂存
        for num in range(self.__CrawlFuncCount__):
            proxyFunc = self.__CrawlFunc__[num]  # 可扩展的不同抓取函数
            try:
                for proxy in eval(f"self.{proxyFunc}()"):  # 迭代
                    logger.info('Crawl From %s - %s',
                                proxyFunc.split('_')[1], proxy)
                    proxies.append(proxy)
            except:
                logger.error(
                    f'Meet error when fetching proxy from {proxyFunc}', exc_info=True)
            if proxies:
                for proxy in proxies:
                    self.redis.add(CHAOS_REDIS_KEY, proxy)  # 置入混沌池，进行清洗

    def srtweb(self, url):
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

    def crawl_Xila(self):
        start_url = "http://www.xiladaili.com/gaoni/{}/"

        for page in range(1, CRAWL_PAGES+1):
            html = self.srtweb(start_url.format(page))

            if html is not None:  # 正确获得返回数据
                for x in range(1, 50 + 1):
                    Tpproxy = html.xpath(
                        f"//tbody/tr[{x}]/td[position()<3]/text()")
                    if PROXY_TYPE in [proxy.replace('代理', '') for proxy in Tpproxy[1].split(',')]:
                        yield Tpproxy[0]
            time.sleep(random.uniform(1, 3))

    def crawl_Xici(self):
        start_url = "https://www.xicidaili.com/nn/{}"

        for page in range(1, CRAWL_PAGES+1):
            html = self.srtweb(start_url.format(page))

            if html is not None:
                for x in range(1, 100+1):
                    Tpproxy = html.xpath(
                        f"//tr[@class][{x}]/td[position()=2 or position()=3 or position()=6]/text()")
                    if PROXY_TYPE == Tpproxy[2]:
                        proxy = Tpproxy[0] + ':' + Tpproxy[1]
                        yield proxy
            time.sleep(random.uniform(1, 3))

    def crawl_Kuai(self):
        start_url = "https://www.kuaidaili.com/free/inha/{}/"

        for page in range(1, CRAWL_PAGES+1):
            html = self.srtweb(start_url.format(page))

            if html is not None:
                for x in range(1, 15+1):
                    Tpproxy = html.xpath(
                        f"//tr[{x}]/td[position()=1 or position()=2 or position()=4]/text()")
                    if PROXY_TYPE == Tpproxy[2]:
                        proxy = Tpproxy[0] + ':' + Tpproxy[1]
                        yield proxy
            time.sleep(random.uniform(1, 3))

    def crawl_yun(self):
        start_url = "http://www.ip3366.net/free/?stype=1&page={}"

        for page in range(1, CRAWL_PAGES+1):
            html = self.srtweb(start_url.format(page))

            if html is not None:
                for x in range(1, 15+1):
                    Tpproxy = html.xpath(
                        f"//tr[{x}]/td[position()=1 or position()=2 or position()=4]/text()")
                    if PROXY_TYPE == Tpproxy[2]:
                        proxy = Tpproxy[0] + ':' + Tpproxy[1]
                        yield proxy
            time.sleep(random.uniform(1, 3))

    def crawl_66(self):
        start_url = "http://www.66ip.cn/{}.html"

        for page in range(1, CRAWL_PAGES+1):
            html = self.srtweb(start_url.format(page))

            if html is not None:
                gData = html.xpath(
                    '//tr[position()!=1]/td[position()<3]/text()')
                num = int(len(gData) / 2)
                for _ in range(num):
                    yield gData[2*_] + ':' + gData[2*_+1]
            time.sleep(random.uniform(1, 3))


crawler = Crawler()
