from .config import *
from .logger import logger
from .db import myredis

import requests
import asyncio


class Validator(object):
    def __init__(self, table):
        self.redis = myredis
        self.table = table

    def native_ip(self):
        # 获取本地ip，用于比对，测试代理的匿名性
        # Returns: str(succeed) / None(failed)
        try:
            json_get = requests.get(IP_QUERY_URL).json()
            native_ip = json_get['origin'].split(',')[0]
            return native_ip
        except:
            logger.error('Fail To Get Native IP', exc_info=True)

    async def judge_tasks(self, proxies_queue):
        while not proxies_queue.empty():
            test_proxy = await proxies_queue.get()
            try:
                logger.info(test_proxy)
                await asyncio.sleep(5)
            except Exception as e:
                logger.error('Error for {}'.format(test_proxy), exc_info=True)

    def run(self):
        try:
            count = self.redis.count(self.table)
            logger.info('Current Number of Proxies: {}'.format(count))

            nativeip = self.native_ip()
            logger.info('Current Native IP: {}'.format(nativeip))
            
            loop = asyncio.get_event_loop()

            for x in range(0, count, VALIDATE_SIZE):
                # Ensure validate all proxies
                start = x + 1
                stop = min(x + VALIDATE_SIZE, count)

                logger.info('Validating {}-{} Proxies'.format(start, stop))
                proxies_list = self.redis.get(  # 从数据库获取proxies
                    self.table,
                    start,
                    stop
                )

                proxies_queue = asyncio.Queue()
                [proxies_queue.put_nowait(proxy) for proxy in proxies_list]
                
                tasks = [self.judge_tasks(proxies_queue)
                         for t in range(stop - x)]
                loop.run_until_complete(asyncio.wait(tasks))
                

        except:
            logger.error('No', exc_info=True)
        finally:
            loop.close()


chaos_validator = Validator(CHAOS_REDIS_KEY)
stable_validator = Validator(STABLE_REDIS_KEY)
