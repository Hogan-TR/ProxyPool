from proxypool.scheduler import Scheduler


def main():
    # 启动调度器
    try:
        task = Scheduler()
        task.run()
    except:
        main()


if __name__ == '__main__':
    main()
