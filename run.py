from proxypool.scheduler import Scheduler
from proxypool.logger import logger


def main():
    # 启动调度器
    try:
        task = Scheduler()
        task.run()
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    main()
