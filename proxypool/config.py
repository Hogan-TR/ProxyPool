import os


# 开启选项 仅调试用 正常运行必须完全开启
SWITCH_CRA = True
SWITCH_VAL = True
SWITCH_API = True


# 相对根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Redis数据库
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASSWORD = None
CHAOS_REDIS_KEY = "chaos"
STABLE_REDIS_KEY = "stable"


# api配置
API_HOST = '0.0.0.0'
API_PORT = '8888'


# 日志
LOG_LEVEL = "INFO"
LOG_FILE = True


# 评分机制
INITIAL_SCORE = 6  # 初始分
MIN_SCORE = 5  # 混沌池最小允许分
MIX_SCORE = 7  # 稳定池最小允许分
MAX_SCORE = 10  # 最大可及分
SATISFY_SCORE = 8  # 迁移条件


# 校验机制
IP_QUERY_URL = 'http://httpbin.org/ip'  # 检测原始IP
# IP_QUERY_URL = 'http://icanhazip.com/'# 备用 / (http://ip.360.cn/IPShare/info)
VALIDATE_SIZE = 50  # 单次校验代理数


# 抓取配置
CRAWL_PAGES = 3  # 抓取数据页
PROXY_TYPE = "HTTP"
UserAgent = [
    "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)",
    "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0; DigExt)",
    "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0; TUCOWS)",
    "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0; by TSG)",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0; .NET CLR 1.0.3705)",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; en) Opera 8.0",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0;)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; T312461)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; en) Opera 8.00",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; TencentTraveler )",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; zh-cn) Opera 8.0",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; zh-cn) Opera 8.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322; FDM)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; Maxthon; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; MathPlayer 2.0; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; {FF0C8E09-3C86-44CB-834A-B8CEEC80A1D7}; iOpus-I-M)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; i-Nav 3.0.1.0F; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.7) Gecko/20040616",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; ja-JP; rv:1.5) Gecko/20031007",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; rv:1.7.3) Gecko/20040913 Firefox/0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; rv:1.7.3) Gecko/20041001 Firefox/0.10.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; ja-JP; m18) Gecko/20010131 Netscape6/6.01",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.7) Gecko/20040803 Firefox/0.9.3",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; de-DE; rv:1.7.5) Gecko/20041108 Firefox/1.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; de-DE; rv:1.7.5) Gecko/20041122 Firefox/1.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.7.5) Gecko/20041107 Firefox/1.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.7.5) Gecko/20041110 Firefox/1.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; fr-FR; rv:1.7.5) Gecko/20041108 Firefox/1.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; it-IT; rv:1.7.5) Gecko/20041110 Firefox/1.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.8b) Gecko/20050118 Firefox/1.0+",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.198 Safari/532.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.6 Safari/532.0",
    "Mozilla/4.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.33 Safari/532.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.55 Safari/525.19",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
]
