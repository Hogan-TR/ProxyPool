from .config import *
from .logger import logger
from .crawler import crawler
from .validator import chaos_validator, stable_validator
from .transfer import transfer
from .api import app


from multiprocessing import Process, Event
import os
import time
import signal


class Scheduler(object):
    def __init__(self):
        self.processes = list()  # 子进程列表
        self.event_1 = Event()  # 进程通信 crawl - validate(chaos)
        self.event_2 = Event()  # transfer - validate(chaos)
        #  注册信号接受函数 子进程继承主进程的信号处理方法
        signal.signal(signal.SIGINT, self.term)  # Ctrl+C / kill -9 pid
        signal.signal(signal.SIGTERM, self.term)  # kill -15 pid

    def run(self):
        logger.info("Start Running Proxy Pool")
        if SWITCH_CRA:  # 抓取
            pcrawl = Process(
                target=self.sch_crawl,
                args=(self.event_1,),
                daemon=True
            )  # 设为守护进程
            pcrawl.start()  # 启动子进程
            self.processes.append(pcrawl)  # 将子进程加入列表

        if SWITCH_VAL:  # 过滤
            pvalidate_chaos = Process(
                target=self.sch_validate_chaos,
                args=(self.event_1, self.event_2),
                daemon=True
            )
            pvalidate_chaos.start()
            self.processes.append(pvalidate_chaos)

            pvalidate_stable = Process(
                target=self.sch_validate_stable,
                daemon=True
            )
            pvalidate_stable.start()
            self.processes.append(pvalidate_stable)

        if SWITCH_CRA and SWITCH_VAL:  # 迁移
            ptransfer = Process(
                target=self.sch_transfer,
                args=(self.event_2,),
                daemon=True
            )
            ptransfer.start()
            self.processes.append(ptransfer)

        if SWITCH_API:  # 接口
            papi = Process(target=self.sch_api, daemon=True)
            papi.start()
            self.processes.append(papi)

        try:
            for p in self.processes:
                p.join()  # 阻塞任务
        except Exception as e:
            logger.error(str(e))

    def term(self, sig, frame):  # 信号处理函数
        logger.info(
            f"Received SIGINT, shutting down gracefully. Current pid is {os.getpid()}, group id is {os.getpgrp()}")
        os.killpg(os.getpgid(os.getpid()), signal.SIGKILL)  # 结束进程组

    def sch_crawl(self, event):
        while True:
            if not event.is_set():
                logger.info("Start Crawling Proxies")
                crawler.run()
                event.set()  # 置 flag 为True
                time.sleep(1800)  # 600
                event.clear()  # 重新置为False

    def sch_validate_chaos(self, event_1, event_2):
        while True:
            if not event_1.is_set():
                event_1.wait()  # 阻塞，等待为True
            if not event_2.is_set():
                event_2.wait()
            logger.info("Start Validating Proxies(chaos)")
            chaos_validator.run()
            event_2.clear()
            time.sleep(60)  # 30 ~ 60

    def sch_validate_stable(self):
        while True:
            logger.info("Start Validating Proxies(stable)")
            stable_validator.run()
            time.sleep(60)

    def sch_transfer(self, event):
        while True:
            if not event.is_set():
                logger.info("Start Transfering Proxies: chaos -> stable")
                transfer.run()
                event.set()

    def sch_api(self):
        logger.info("Start Loading API")
        app.run(API_HOST, API_PORT)
