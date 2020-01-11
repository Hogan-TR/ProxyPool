from .config import *
from .logger import logger

from multiprocessing import Process
import os
import time
import signal


class Crawler(Process):  # 代理抓取
    def __init__(self):
        super(Crawler, self).__init__()

    def run(self):
        pass


class Validator_Chaos(Process):  # 混沌清洗
    def __init__(self):
        super(Validator_Chaos, self).__init__()

    def run(self):
        pass


class Validator_Stable(Process):  # 稳定清洗
    def __init__(self):
        super(Validator_Stable, self).__init__()

    def run(self):
        pass


class Transfer(Process):  # 数据迁移
    def __init__(self):
        super(Transfer, self).__init__()

    def run(self):
        pass


class Api(Process):  # 对外接口
    def __init__(self):
        super(Api, self).__init__()

    def run(self):
        pass


class Scheduler(object):
    def __init__(self):
        self.processes = list()  # 子进程列表
        #  注册信号接受函数 子进程继承主进程的信号处理方法
        signal.signal(signal.SIGINT, self.term)  # Ctrl+C / kill -9 pid
        signal.signal(signal.SIGTERM, self.term)  # kill -15 pid

    def run(self):
        logger.info("Start Running Proxy Pool")
        if SWITCH_CRA:  # 抓取
            pcrawl = Crawler()
            pcrawl.daemon = True  # 设为守护进程
            pcrawl.start()  # 启动子进程
            Processes.append(pcrawl)  # 将子进程加入列表

        if SWITCH_VAL:  # 过滤
            pvalidate_chaos = Validator_Chaos()
            pvalidate_chaos.daemon = True
            pvalidate_chaos.start()
            Processes.append(pvalidate_chaos)

            pvalidate_stable = Validator_Stable()
            pvalidate_stable.daemon = True
            pvalidate_stable.start()
            Processes.append(pvalidate_stable)

        if SWITCH_CRA and SWITCH_VAL:  # 迁移
            ptransfer = Transfer()
            ptransfer.daemon = True
            ptransfer.start()
            Processes.append(ptransfer)

        if SWITCH_API:  # 接口
            papi = Api()
            papi.daemon = True
            papi.start()
            Processes.append(papi)

        try:
            for p in self.processes:
                p.join()  # 阻塞任务
        except Exception as e:
            logger.error(str(e))

    def term(self, sig, frame):  # 信号处理函数
        logger.info(
            f"Current pid is {os.getpid()}, group id is {os.getpgrp()}")
        os.killpg(os.getpgid(os.getpid()), signal.SIGKILL)  # 结束进程组
