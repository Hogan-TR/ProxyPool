from .config import *
from .logger import logger
from .db import myredis

import requests
import asyncio
import aiohttp


class Validator(object):
    def __init__(self, table):
        self.redis = myredis
        self.table = table
        self.loop = asyncio.get_event_loop()

    def native_ip(self):
        # 获取本地ip，用于比对，测试代理的匿名性
        # Returns: str(succeed) / None(failed)
        try:
            json_get = requests.get(IP_QUERY_URL).json()
            native_ip = json_get['origin'].split(',')[0]
            return native_ip
        except:
            logger.error('Fail To Get Native IP', exc_info=True)

    async def fetch(self, session, proxy, res_queue) -> dict:
        async with session.get(IP_QUERY_URL, proxy='http://{}'.format(proxy), timeout=30) as response:
            status_code = response.status
            if status_code != 200:  # 第一层 - 检查状态码
                raise Exception
            return await response.json()

    async def parse(self, proxy, native_ip, data, res_queue):
        MaskedIP = data['origin'].split(',')[0]
        if native_ip != MaskedIP:
            res_queue.put_nowait((proxy, True))
            logger.info('Validating Proxy - {} | √'.format(proxy))
        else:
            res_queue.put_nowait((proxy, False))
            logger.info('Validating Proxy - {} | ×'.format(proxy))

    async def judge_tasks(self, proxies_queue, res_queue, native_ip):
        while not proxies_queue.empty():
            test_proxy = await proxies_queue.get()
            try:
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                    fetch_get = await self.fetch(session, test_proxy, res_queue)
                    await self.parse(test_proxy, native_ip, fetch_get, res_queue)
            except Exception as e:
                res_queue.put_nowait((test_proxy, False))
                logger.info('Validating Proxy - {} | ×'.format(test_proxy))

    def run(self):
        try:
            count = self.redis.count(self.table)
            logger.info('Current Number of Proxies: {}'.format(count))

            nativeip = self.native_ip()
            logger.info('Current Native IP: {}'.format(nativeip))

            proxies_queue = asyncio.Queue()  # 待办队列
            res_queue = asyncio.Queue()  # 结果队列

            for x in range(0, count, VALIDATE_SIZE):
                # Ensure validate all proxies
                start = x + 1
                stop = min(x + VALIDATE_SIZE, count)

                proxies_list = self.redis.get(  # 从数据库获取proxies
                    self.table,
                    start,
                    stop
                )
                if proxies_list is not None:
                    logger.info('Validating {}-{} Proxies'.format(start, stop))
                    [proxies_queue.put_nowait(proxy) for proxy in proxies_list]
                    tasks = [self.judge_tasks(proxies_queue, res_queue, nativeip)
                             for t in range(stop - x)]
                    self.loop.run_until_complete(asyncio.wait(tasks))

            while not res_queue.empty():
                proxy, res = res_queue.get_nowait()
                if res:
                    self.redis.increase(self.table, proxy)
                else:
                    self.redis.decrease(self.table, proxy)

        except:
            logger.error('Unknown Error', exc_info=True)


chaos_validator = Validator(CHAOS_REDIS_KEY)
stable_validator = Validator(STABLE_REDIS_KEY)
