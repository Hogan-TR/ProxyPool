from .config import *
from .logger import logger
from .db import myredis

import requests


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

    def run(self):
        try:
            count = self.redis.count(self.table)
            logger.info('Current Number of Proxies: {}'.format(count))

            nativeip = self.native_ip()
            logger.info('Current Native IP: {}'.format(nativeip))

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

                from pprint import pprint
                pprint(proxies_list)

        except:
            pass


chaos_validator = Validator(CHAOS_REDIS_KEY)
stable_validator = Validator(STABLE_REDIS_KEY)
