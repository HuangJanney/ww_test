import sys, os
import re
import ast

from BeautifulReport import BeautifulReport

cur_path = os.getcwd()
sys.path.append(cur_path[:cur_path.find('ww_test') + len('ww_test')])
import unittest
from page.main_page import MainPage
import time
from utils.excel_util import ExcelReader
from utils.file_util import FileUtil
from utils.config_util import ConfigUtil
from utils.image_util import ImageUtil
from ddt import ddt,data,unpack

@ddt
class TestSmoking(unittest.TestCase):
    # backpack = BackpackPage()
    # image = ImageUtil()
    page = MainPage()
    # config= ConfigUtil()
    


    # @classmethod
    # def setUpClass(cls):
    #     cls.page.start_recording()
    @data(*ExcelReader("0.3.5制造台配方.xls").get_column_values('物品ID',start_row=1))
    def test_01(self,itemid):
        if itemid == "":
            pass
        else:
            # itemid= str(itemid).rstrip('0').rstrip('.')
            itemid = str(itemid).rstrip('0').rstrip('.') if '.' in str(itemid) else str(itemid)
            print(itemid)
            self.page.learn_by_goods(itemid)
            self.page.get_material(itemid)
            # self.page.making()
            self.page.make_by_craft_station(itemid,False)
            self.page.clean_backpack()

    # @classmethod
    # def tearDownClass(cls):
    #     cls.page.stop_recording('furniture.mp4','recoder')



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