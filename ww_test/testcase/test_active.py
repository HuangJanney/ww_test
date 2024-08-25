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
class TestActive(unittest.TestCase):
    page = MainPage()

    


    # @classmethod
    # def setUpClass(cls):
        # # cls.page.start_test()
        # cls.page.start_game_now()
        # cls.page.poco_gm('operate_reinforce')

    # @data(*ExcelReader("0.3.4版本商城app五官副本.xls").get_column_values('物品id',start_row=1))

    # def test_01(self):
    #     '''强金币'''
    #     for i in range(1000):
    #         for direction in ["W","A","S","D"]:
    #             self.page.move_stick(direction)
    #             if self.page.poco_exists('ui://pkg_icon/image/money/small_icon_07'):
    #                 self.page.poco_click('ui://pkg_icon/image/money/small_icon_07')
                    # self.page.input_text()

    # def test_02(self):
    #     for i in range(10000):
    #         player_list = ["mumu","player1048909","player1052390","player1052388"]
    #         for player in player_list:
    #             self.page.poco_click_bytext(player)
    #             self.page.poco('input').click()
    #             self.page.sleep()
    #             self.page.input_text("congratulations")
    #             self.page.sleep()
    #             self.page.touch_coord(0.2,0.2)
    #             self.page.poco(text="发送").click()

    def test_03(self):
        '''钓鱼'''
        for i in range(100):
            self.page.fishing()
            while True:
                if self.page.exists_recursively_default('fishing1.png'):
                    self.page.fish()
                    self.page.sleep()
                    if self.page.poco_exists_bytext('收下'):
                        self.page.poco_click_bytext('收下')
                        self.page.sleep()
                        break
                elif self.page.poco_exists_bytext('收下'):
                        self.page.poco_click_bytext('收下')
                        self.page.sleep()
                        break
                    







if __name__ == '__main__':
    unittest.main()
    # now = time.strftime("%Y-%m-%d %H%M%S", time.localtime(time.time()))
    # ts = unittest.TestSuite()  # 实例化
    # # 按类加载全部testxxx测试用例   
    # ts.addTest(unittest.makeSuite(TestSuit))
    # # 按函数加载testxxx测试用例
    # # ts.addTest(HtmlReport('test_1'))
    # report_name = '商城app五官测试'
    # filename = report_name + now + '.html'
    # # 加载执行用例生成报告
    # result = BeautifulReport(ts)
    # # 定义报告属性
    # result.report(description='商城app五官测试', filename=filename, report_dir=FileUtil.get_report_path())
    # print(FileUtil.get_report_path())