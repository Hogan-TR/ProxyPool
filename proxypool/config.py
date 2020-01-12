# 开启选项
SWITCH_CRA = True
SWITCH_VAL = True
SWITCH_API = True

# Redis数据库
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASSWORD = None
CHAOS_REDIS_KEY = "chaos"
STABLE_REDIS_KEY = "stable"

# 评分机制
INITIAL_SCORE = 5  # 初始分
MIX_SCORE = 7  # 稳定池最小允许分
MAX_SCORE = 10  # 最大可及分

# 抓取配置
CRAWL_PAGES = 3  # 抓取数据页
