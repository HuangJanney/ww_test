# 导入所需的模块
import time
import datetime
from airtest.core.api import *
# from airtest.core.android.recorder import *
from airtest.core.android.adb import *
import sys, os


from BeautifulReport import BeautifulReport

cur_path = os.getcwd()
sys.path.append(cur_path[:cur_path.find('ww_test') + len('ww_test')])
import unittest
from page.main_page import MainPage
import time
from utils.file_util import FileUtil
from utils.config_util import ConfigUtil
from utils.image_util import ImageUtil

class TestRecoder(unittest.TestCase):
    # backpack = BackpackPage()
    # image = ImageUtil()
    page = MainPage()
    # config= ConfigUtil()
    


    # @classmethod
    # def setUpClass(cls):
    #     # cls.page.start_test()
    #     cls.page.start_test_new()
    def test_01(self):
        # 定义手机录屏的开始和结束时间
        start_time = datetime.datetime(2024, 2, 22, 10, 33, 0) # 年，月，日，时，分，秒
        end_time = datetime.datetime(2024, 2, 22, 10, 35, 0)
        # 获取当前时间
        now = datetime.datetime.now()

        # 等待开始时间到达
        while now < start_time:
            time.sleep(1)
            print(now)
            now = datetime.datetime.now()

        # 开始录制手机屏幕
        self.page.start_recording()
        while now < end_time:
            self.page.sleep(1)
            print(now)
            now = datetime.datetime.now()
        self.page.stop_recording('task.mp4','recoder')




if __name__ == '__main__':
    unittest.main()