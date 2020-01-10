from .config import *
from .logger import logger
import redis
import re


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """与Redis服务器建立连接

        Args:
            host: Redis服务器ip
            port: Redis服务器对应端口
            password: Redis服务器密码
        """
        self.db = redis.StrictRedis(
            host=host, port=port, password=password, decode_responses=True)
        # decode_responses:True  -> 以str类型写入
        # decode_responses:False -> 以byte类型写入

    def count(self, table):
        """获取代理数量

        Args:
            table: 数据库名称(此工程至少有两个数据库)

        Returns:
            返回数据库中的数据量(int)
            for example: 100
        """
        return self.db.zcard(table)

    def add(self, table, proxy, score=INITIAL_SCORE):
        """添加代理

        Args:
            table: 处理数据库名称
            proxy: 代理信息
            score: 代理初始分(默认为config中的INITIAL_SCORE)

        Returns:
            1(int): 成功添加一条代理信息
            None(NoneType): 代理格式不匹配或此代理已存在数据库
        """
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):  # 正则匹配 代理ip
            logger.error('Irregular Format | Proxy - %s', proxy)
            return  # NoneType
        if not self.db.zscore(table, proxy):  # 未进入池中
            mapping = {
                proxy: score,
            }
            return self.db.zadd(table, mapping)  # 加入池

    def increase(self, table, proxy):
        """代理加分
        一次性仅加一分

        Args:
            table: 待处理数据库名称
            proxy: 待加分代理项

        Returns:
            scores(float): 加分后代理分
            None(NoneType): 代理分已达最大分
        """
        score = self.db.zscore(table, proxy)
        if score and score < MAX_SCORE:
            return self.db.zincrby(table, 1, proxy)
        else:
            return

    def decrease(self, table, proxy):
        """代理减分/删除

        Args:
            table: 待处理数据库名称
            proxy: 待减分/删除代理项

        Returns:
            scores(float): 减分后代理分
            1(int): 删除无效代理
        """
        score = self.db.zscore(table, proxy)

        # 稳定代理数据池与临时数据池采取不同处理
        if table == STABLE_REDIS_KEY:
            if score and score > INITIAL_SCORE:
                return self.db.zincrby(table, -1, proxy)  # 减分
            else:
                return self.db.zrem(table, proxy)  # 删除
        else:
            if score and score > MIN_SCORE:
                return self.db.zincrby(table, -1, proxy)  # 减分
            else:
                return self.db.zrem(table, proxy)  # 删除

    # def get(self, table, start=0, stop=-1):
    #     # 默认获取所有代理
    #     # 若获取单个代理：start = 0, stop = 0
    #     # free获取代理：start = value, stop = value
    #     result = self.db.zrevrange(table, start, stop)
    #     if result:
    #         return result
    #     else:
    #         return

    # def score(self, table, proxy):
    #     score = self.db.zscore(table, proxy)
    #     if score:
    #         return score
    #     else:
    #         return


myredis = RedisClient()
