# ProxyPool
🛠一款**异步**清洗、高效抓取、稳定提供有效代理的**IP代理池**。



## 特点

- 将混沌池（原始数据）与稳定池（面向用户的优质数据）相**分离**，保证代理池在任意时刻提供代理的高效、可用
- 采取**差异评分**机制，对不同池制定不同筛选标准，有效淘汰成功率较低的代理
- 通过 Python 的神奇语法糖，仅需数行代码，即可完成抓取**函数**的自由**注册**
- 在不同子进程间建立**通信**，确保代理池正常运转的同时，进程能够自主有序运行



## 运行

#### Docker部署

1. `Docker` + `docker-compose` 安装

3. 下载当前仓库代码到本地

   ```
   git clone https://github.com/Hogan-TR/ProxyPool.git
   ```

3. 修改 `./proxypool/config.py` 中的配置

   ```python
   # 将 REDIS_HOST 的内容替换为当前机器的内网ip
   REDIS_HOST = "127.0.0.1"
   # 若本地有 redis 环境，可将容器 redis 端口更改为6399
   REDIS_PORT = 6399
   
   # 其他配置默认无需更改
   ```

4. 修改 `docker-compose.yml` 中的配置

   ```python
   # 可修改 main 中 ports 的端口映射，从而更改 api 的本地调用接口，默认5000端口
   main:
       ...
       ports:
           - "5000:5000"
       ...
       
   # 若上步修改 reids 端口，则此处需修改端口映射
   db:
       ...
       ports:
           - "6399:6379"
       ...
   ```
   
5. 执行 `docker-compose up` ，启动代理池

#### 基于本机环境部署(仅支持类Unix系统)

1. 准备：`Python3` + `Redis` 环境

2. 下载当前仓库代码到本地

   ```
   git clone https://github.com/Hogan-TR/ProxyPool.git
   ```

3. 创建虚拟环境，安装依赖

   ```shell
   cd ProxyPool
   python3 -m venv venv
   source ./venv/bin/activate
   pip install -r requirements.txt
   ```

4. 根据系统 Redis 配置修改 `./proxypool/config.py` 中 Redis 相关参数`REDIS_HOST`，`REDIS_PORT`，`REDIS_PASSWORD`

5. 执行 `sudo python run.py` 命令，启动代理池

**注：代理池首次启动后需十分钟左右，进行数据的抓取、清洗，才可开始提供高质代理；本地默认调用➡[接口](http://localhost:5000/ "http://localhost:5000/")**



## 功能实现

![](diagrame.png "Architecture diagram")



## 配置

```python
# .proxypool/config.py

# 开启选项 仅调试用 正常运行必须完全开启
SWITCH_CRA = True    # crawler模块
SWITCH_VAL = True    # validator模块
SWITCH_API = True    # api模块


# 相对根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Redis数据库
REDIS_HOST = "127.0.0.1"      # IP
REDIS_PORT = 6379             # 端口 若以容器启动，并且本地有redis环境
REDIS_PASSWORD = None         # 密码
CHAOS_REDIS_KEY = "chaos"     # 混沌池 —— sorted set | 注：池的key默认无需更改
STABLE_REDIS_KEY = "stable"   # 稳定池 同上


# api配置
API_HOST = '0.0.0.0'
API_PORT = '5000'


# 日志
LOG_LEVEL = "INFO"  # 日志等级 实际使用可置为"WARNING"
LOG_FILE = True     # 是否保存日志文件


# 评分机制
INITIAL_SCORE = 6   # 初始分
MIN_SCORE = 5       # 混沌池最小允许分
MIX_SCORE = 7       # 稳定池最小允许分
MAX_SCORE = 10      # 最大可及分
SATISFY_SCORE = 8   # 迁移条件


# 抓取配置
CRAWL_PAGES = 3       # 单资源站抓取数据页
PROXY_TYPE = "HTTP"   # 代理类型
UserAgent = [         # 伪造请求头
    ...
]


# 校验机制
IP_QUERY_URL = 'http://httpbin.org/ip'   # 校验目标对象
VALIDATE_SIZE = 50                       # 单次校验代理数
# IP_QUERY_URL = 'http://icanhazip.com/'
# IP_QUERY_URL = 'http://ip.360.cn/IPShare/info'
# 备用检验地址，同时校验方式需随之改变
```



## 代理扩展

对于网络上不同代理资源的时效性和差异性,此代理池在 `crawler` 模块中通过装饰器 `crawler.register` 实现对抓取函数的**注册**,仅需传入请求地址的格式化字符串,例如 `http://www.xiladaili.com/gaoni/{}/`, 再对每个具体页请求返回的**结构化树** `html` 进行数据提取,最后以**生成器**的方式返回，即可将数据写入数据库进行验证

```python
# .proxypool/crawler.py
...
# 类实例化,并且将抓取函数注册到类的funcs列表中
crawler = Crawler()  


@crawler.register("http://www.xiladaili.com/gaoni/{}/")
def crawl_Xila(html):
    for x in range(1, 50 + 1):
        Tpproxy = html.xpath(f"//tbody/tr[{x}]/td[position()<3]/text()")
        if PROXY_TYPE in [proxy.replace('代理', '') for proxy in Tpproxy[1].split(',')]:
            yield Tpproxy[0]
            
# 装饰器传入请求页模板,{}中为工作页数,可在config配置总获取页数 -> CRAWL_PAGES
# 被装饰函数形参目前必须为 "html" => 经处理的结构化网页
# 此示例中用 xpath 来提取数据
# 生成器每次返回字符串对象 如: "100.100.100.100:9999"
```



## API

**介绍页**

> ```json
> 请求示例
> http://localhost:5000/proxypool/
> 
> 响应示例
> {
>  "count": "Get num of proxies",
>  "get": "Get one of best proxies randomly",
>  "get_all": "Get all proxies",
>  "get_all_ws": "Get all proxies with scores"
> }
> ```

**池现存量**

> ```json
> 请求示例
> http://localhost:5000/proxypool/count
> 
> 响应示例
> {
>  "count_chaos": 1569,
>  "count_stable": 270
> }
> ```

**随机最优代理**

> ```json
> 请求示例
> http://localhost:5000/proxypool/get
> 
> 响应示例
> {
>     "proxy": "59.56.28.199:80"
> }
> ```

**获取所有代理**

> ```json
> 请求示例
> http://localhost:5000/proxypool/get_all
> 
> 响应示例
> {
>  "proxies": [
>      "78.46.91.48:1080",
>      "59.56.28.254:80"
>  ]
> }
> ```

**获取所有代理 with score**

> ```json
> 请求示例
> http://localhost:5000/proxypool/get_all_ws
> 
> 响应示例
> {
>     "proxies": [
>         [
>             "78.46.91.48:1080",
>             10.0
>         ],
>         [
>             "59.56.28.254:80",
>             10.0
>         ]
>     ]
> }
> ```

**异常处理**

> ```json
> 响应示例
> {
>     "error": "Not found"
> }
> ```



## TODO

- [ ] 单次启动，提供不同类型代理(受限于 `aiohttp` 对 `https` 的支持性，考虑改用 `httpx` 进行异步验证)
- [ ] 激进的进程调度策略，进一步提高效率
