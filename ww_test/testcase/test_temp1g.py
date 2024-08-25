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
    # backpack = BackpackPage()
    # image = ImageUtil()
    page = MainPage()
    # config= ConfigUtil()
    


    # @classmethod
    # def setUpClass(cls):
    #     # cls.page.start_test()
    #     cls.page.start_test_new()
    def test_01(self):
        # self.page.login()
        # self.page.sign_up()
        # self.page.rookie_guide()
        # self.page.buy_from_shota('50100003')
        # self.page.start_party(2)
        # self.page.close_party()
        # self.page.sing_in()
        # a = self.config.get_yaml_value('position.yaml','rookie_guide','Stone1')
        # print(a)
        # print(type(a))
        # points = ast.literal_eval(a)

        # print(points)
        # print(type(points))
        # self.page.poco('ui://pkg_icon/image/gameuiicon/avatar/clothing/login_iconb_14n').click()
        # self.page.capture_poco('backapckbody','test.png')
        # self.page.poco_gm('clean_all_jiaju')
        self.page.poco_gm('operate_reinforce')
        # self.page.poco_gm('operate_reinforce')
        # a = self.page.poco('ui://pkg_mainwindow/image/house_icon_tap')
        # print(type(a))
        # # print(a[1])
        # is_last_iteration = False
        # for index,i in enumerate(a) :
        #     print(i)
        #     print(index)
        #     i.click()
        #     self.page.move_stick("W")
        #     try:
        #         _ = next(iter(a[index+1:]))
        #     except IndexError:
        #         is_last_iteration = True
        #         print('10000')
        # self.page.poco_click('ui://2ni11kbwulg78yjc')
        # a[0].click()
        # self.page.preview_clothes('71100114')
        # self.page.capture_poco('ui://pkg_icon/image/suit/icon_earjewelry_006_c','suit_test.png','cut')
        # self.page.get_material('90104001')
        # self.page.make_by_craft_station('90104001')
        # self.page.move_star(20,10)
        # self.page.get_fabricate('90204046')
        pass



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