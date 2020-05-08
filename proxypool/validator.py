from .config import IP_QUERY_URL, CHAOS_REDIS_KEY, STABLE_REDIS_KEY, VALIDATE_SIZE
from .logger import logger
from .db import myredis

import requests
import asyncio
import aiohttp


class Validator(object):
    def __init__(self, table):
        self.redis = myredis
        self.table = table
        self.res_list = []

    def native_ip(self):
        # 获取本地ip，用于比对，测试代理的匿名性
        # Returns: str(succeed) / None(failed)
        try:
            json_get = requests.get(IP_QUERY_URL).json()
            native_ip = json_get['origin'].split(',')[0]
            return native_ip
        except:
            logger.error('Fail To Get Native IP', exc_info=True)

    async def fetch(self, session, proxy) -> dict:
        async with session.get(IP_QUERY_URL, proxy='http://{}'.format(proxy), timeout=30) as response:
            status_code = response.status
            if status_code != 200:  # 第一层 - 检查状态码
                raise Exception
            return await response.json()

    def parse(self, proxy, native_ip, data):
        MaskedIP = data['origin'].split(',')[0]
        if native_ip != MaskedIP:
            return True
        else:
            return False

    async def judge_task(self, proxy, native_ip):
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                fetch_get = await self.fetch(session, proxy)
                if self.parse(proxy, native_ip, fetch_get):
                    logger.info('Validating Proxy - {} | √'.format(proxy))
                    return proxy, True
                else:
                    logger.info('Validating Proxy - {} | ×'.format(proxy))
                    return proxy, False
        except Exception:  # incorrect status_code or timeout
            logger.info('Validating Proxy - {} | ×'.format(proxy))
            return proxy, False

    async def gather(self, *tasks):
        sub_res = await asyncio.gather(*tasks)
        # just put into global list, refresh redis-data lastly
        self.res_list.extend(sub_res)
        logger.info(sub_res)

    def run(self):
        try:
            count = self.redis.count(self.table)
            logger.info('Current Number of Proxies: {}'.format(count))

            # TODO
            if count == 0:
                pass  # end this loop

            # proxies_list => [] that contain all proxies
            proxies_list = self.redis.get(self.table)
            # grouping proxies list => [[], [], ...]
            proxies_group = [proxies_list[m:m+VALIDATE_SIZE]
                             for m in range(0, count, VALIDATE_SIZE)]

            nativeip = self.native_ip()
            logger.info('Current Native IP: {}'.format(nativeip))

            for index, sub_proxies_list in enumerate(proxies_group):
                begin, end = index * VALIDATE_SIZE + 1, index * \
                    VALIDATE_SIZE + len(sub_proxies_list)
                logger.info('Validating {}-{} Proxies'.format(begin, end))

                # build *aws
                proxies_tasks = [self.judge_task(proxy, nativeip)
                                 for proxy in sub_proxies_list]
                asyncio.run(self.gather(*proxies_tasks))

            # all validated and refresh redis-data lastly
            for proxy, res in self.res_list:
                if res:
                    self.redis.increase(self.table, proxy)
                else:
                    self.redis.decrease(self.table, proxy)

        except:
            logger.error('Unkown Error', exc_info=True)


chaos_validator = Validator(CHAOS_REDIS_KEY)
stable_validator = Validator(STABLE_REDIS_KEY)
