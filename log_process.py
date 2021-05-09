import logging


def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


@singleton
class Logger():
    def __init__(self, logfile=None):
        self.logger = logging.getLogger()
        # 写日志文件
        logfile = 'flogfile.log'
        file_handler = logging.FileHandler(logfile, mode='a')
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d] - %(message)s"
            ))
        file_handler.setLevel(logging.DEBUG)

        # 向控制台写日志
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)


logger = Logger().logger
