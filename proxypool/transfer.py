from .config import CHAOS_REDIS_KEY, STABLE_REDIS_KEY, SATISFY_SCORE
from .logger import logger
from .db import myredis


class Transfer(object):
    def __init__(self):
        self.redis = myredis

    def run(self):
        proxies = self.redis.get(CHAOS_REDIS_KEY)

        if proxies is not None:
            for p in proxies:
                ts = self.redis.score(CHAOS_REDIS_KEY, p)
                if ts and ts >= SATISFY_SCORE:
                    self.redis.add(STABLE_REDIS_KEY, p, ts)
                else:
                    pass


transfer = Transfer()
