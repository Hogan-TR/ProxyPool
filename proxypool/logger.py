import logging
import sys


def set_log():
    """
    创建日志实例
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)  # 日志等级

    # Handler
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


logger = set_log()
