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
from utils.excel_util import ExcelReader
from ddt import ddt,data,unpack
from utils.log_util import logger

@ddt
class TestFabricate(unittest.TestCase):
    page = MainPage()

    


    # @classmethod
    # def setUpClass(cls):
        # # cls.page.start_test()
        # cls.page.start_game_now()
        # cls.page.poco_gm('operate_reinforce')

    @data(*ExcelReader("0.3.4版本商城app五官副本.xls").get_column_values('物品id',start_row=1))
    def test_01(self,itemid):
        # print("------")
        if itemid == "":
            pass
        else:
            # itemid= str(itemid).rstrip('0').rstrip('.')
            itemid = str(itemid).rstrip('0').rstrip('.') if '.' in str(itemid) else str(itemid)
            print(itemid)
            icon = self.page.get_value_by_id(itemid,'图标')
            part = self.page.get_value_by_id(itemid,'部位')
            self.page.add_item(itemid)
            self.page.preview_clothes(itemid)
            suit_file = f'{part}_{itemid}.png'
            self.page.snapshot_img(suit_file,'test_suit','img')
            self.page.capture_poco(icon,suit_file,'test_suit','icon')






if __name__ == '__main__':
    # unittest.main()
    now = time.strftime("%Y-%m-%d %H%M%S", time.localtime(time.time()))
    ts = unittest.TestSuite()  # 实例化
    # 按类加载全部testxxx测试用例   
    ts.addTest(unittest.makeSuite(TestFabricate))
    # 按函数加载testxxx测试用例
    # ts.addTest(HtmlReport('test_1'))
    report_name = '商城app五官测试'
    filename = report_name + now + '.html'
    # 加载执行用例生成报告
    result = BeautifulReport(ts)
    # 定义报告属性
    result.report(description='商城app五官测试', filename=filename, report_dir=FileUtil.get_report_path())
    print(FileUtil.get_report_path())