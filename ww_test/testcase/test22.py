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
from ddt import ddt,data,unpack
from utils.log_util import logger


class ATest():
    page = MainPage()
    def test_01(self,itemid):
            self.page.move((71.58,32.13))
            self.page.clean_backpack()
            self.page.add_backpack(itemid)
            self.page.open_backpack()
            goods_icon = self.page.get_value_by_id(itemid,'图标')
            self.page.poco_click(goods_icon)
            self.page.back()
            self.page.sleep()
            self.page.place()
            self.page.sleep(2.0)#避免网络波动影响，此处设置2s等待
            place_file = f'{itemid}_place.png'
            self.page.snapshot_img(place_file,'test_furbiture','place')
            #此处进行放置后的截图
            in_use_file = f'{itemid}_inuse.png'
            if self.page.poco_exists('ui://pkg_mainwindow/image/house_icon_fabricate'):
                self.page.poco_click('ui://pkg_mainwindow/image/house_icon_fabricate')
                self.page.sleep(1.0)
                self.page.snapshot_img(in_use_file,'test_furbiture','in_use')
                self.page.back()
                self.page.snapshot_img(in_use_file,'test_furbiture','stop_use')
                
            elif self.page.poco_exists('ui://pkg_mainwindow/image/house_icon_tap'):
                seat_list = self.page.poco('ui://pkg_mainwindow/image/house_icon_tap')
                not_last_iteration = True
                for index,seat in enumerate(seat_list):
                    seat.click()
                    sat_file = f'{itemid}_inuse_{index}.png'
                    # self.page.poco_click('ui://pkg_mainwindow/image/house_icon_tap')
                    self.page.sleep(1.0)
                    self.page.snapshot_img(sat_file,'test_furbiture','in_use')
                    for direction in ["W","A","S","D"]:
                        self.page.move_stick(direction)
                    self.page.snapshot_img(sat_file,'test_furbiture','stop_use')
                    try:
                        _ = next(iter(seat_list[index+1:]))
                    except :
                        not_last_iteration = False
                    current_position = self.page.get_current_position()
                    if current_position[0] == 0 :
                        logger.info(f'{itemid}挂点{index}异常')
                        self.page.poco_click('ui://2ni11kbwulg78yjc')
                        self.page.move((55.76,31.68))
                        if not_last_iteration:
                            self.page.move((71.58,32.13))
                
                
            elif self.page.poco_exists('ui://pkg_mainwindow/image/house_icon_dressing'):
                self.page.poco_click('ui://pkg_mainwindow/image/house_icon_dressing')
                self.page.sleep(1.0)
                self.page.snapshot_img(in_use_file,'test_furbiture','in_use')
                self.page.back()
                self.page.snapshot_img(in_use_file,'test_furbiture','stop_use')
                
            elif self.page.poco_exists('ui://pkg_mainwindow/image/house_icon_cooking'):
                self.page.poco_click('ui://pkg_mainwindow/image/house_icon_cooking')
                self.page.sleep(1.0)
                self.page.snapshot_img(in_use_file,'test_furbiture','in_use')
                self.page.back()
                self.page.snapshot_img(in_use_file,'test_furbiture','stop_use')
            else:
                self.page.snapshot_img(in_use_file,'test_furbiture','fail')
            self.page.poco_gm('clean_all_jiaju')
            logger.info('家具已清除')
        # except:
        #     erro_file_name = '%s_error.png'%itemid
        #     self.page.snapshot_img(erro_file_name,'test_furniture','error')
        #     self.page.stop_game_now()
        #     self.page.start_game_now()
        #     self.page.poco_gm('clean_all_jiaju')
        #     self.page.poco_gm('operate_reinforce')





ATest().test_01("90108031")