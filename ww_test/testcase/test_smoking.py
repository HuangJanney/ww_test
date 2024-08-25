import sys, os
import re
import ast
from BeautifulReport import BeautifulReport
cur_path = os.getcwd()
sys.path.append(cur_path[:cur_path.find('ww_test') + len('ww_test')])
import unittest
from page.main_page import MainPage
import time
from utils.file_util import FileUtil
from utils.config_util import ConfigUtil
from utils.image_util import ImageUtil

class TestSmoking(unittest.TestCase):
    page = MainPage()

    


    # @classmethod
    # def setUpClass(cls):
    #     # cls.page.start_test()
    #     cls.page.start_test_new()

    def test_01(self):
        '''主界面各入口检查'''
        self.assertTrue(self.page.poco_exists_bytext("好友"))


    def test_02(self):
        '''虚拟手机各app完整检查'''

    def test_03(self):
        ''''''
        




if __name__ == '__main__':
    unittest.main()
    # now = time.strftime("%Y-%m-%d %H%M%S", time.localtime(time.time()))
    # ts = unittest.TestSuite()  # 实例化
    # # 按类加载全部testxxx测试用例
    # for i in range(1):        
    #     ts.addTest(unittest.makeSuite(TestSmoking))
    # # 按函数加载testxxx测试用例
    # # ts.addTest(HtmlReport('test_1'))
    # report_name = '对比测试1'
    # filename = report_name + now + '.html'
    # # 加载执行用例生成报告
    # result = BeautifulReport(ts)
    # # 定义报告属性
    # # result.report(description='对比测试1', filename=filename, report_dir=FileUtil.get_report_path())
    # # print(FileUtil.get_report_path())