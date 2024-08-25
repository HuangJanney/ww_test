import time
import logging
from utils.file_util import FileUtil


class Logger(object):

    def __init__(self):
        self.logger = logging.getLogger('ww_test')
        self.logger.setLevel(level=logging.DEBUG)
        cur_time = time.strftime("%Y%m%d%H%M", time.localtime())
        filename = 'test_%s.log' % cur_time
        log_path = FileUtil.get_log_path(filename)
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s]<%(name)s> %(message)s')
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(level=logging.DEBUG)
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level=logging.DEBUG)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def error(self, msg):
        self.logger.error(msg)


logger = Logger()
