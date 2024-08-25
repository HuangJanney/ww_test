import ast
from airtest.core.api import *
from base.base_airtest import BaseAirtest
from utils.excel_util import FolderQuery
from utils.log_util import logger
import re
import math
from utils.config_util import ConfigUtil

class MainPage(BaseAirtest):

    def __init__(self):
        auto_setup(__file__)
        # self.device = connect_device('Android:///')
        self.device = self.set_device()
        # self.device = connect_device("Windows:///?title_re=HiFunClien")
        # self.screen_width = self.device.display_info["height"]
        # self.screen_height = self.device.display_info["width"]
        self.screen_width,self.screen_height = self.get_screen_width()
        super().__init__()


    '''poco对ww常用页面元素操作打包'''
    #获取当前位置(输出为list仅保留x与z，精确到2位小数)
    def get_current_position(self):
        pos = self.select_by_gm('get_pos').split(',')
        current_position = [float(x) for i, x in enumerate(pos) if i != 1]
        return current_position
        



    #向指定坐标移动
    def move(self,position):
        if not isinstance(position,(list,tuple)):
            position = [position]
        formatted_poslist = []
        for point in position:
            if isinstance(point, (int,float)):
                formatted_pos = f"{point}"
            else:
                formatted_pos = f"{point[0]},{point[1]}"
            formatted_poslist.append(formatted_pos)
        if len(formatted_poslist) == 2:
            if len(formatted_poslist[0].split(',')) == 2:
                poslist_str = '_'.join(formatted_poslist)
                last_position = [float(num) for num in formatted_poslist[-1].split(',')]
            else:
                poslist_str = ','.join(formatted_poslist)
                last_position = [float(num) for num in formatted_poslist]
        else:
            poslist_str = '_'.join(formatted_poslist)
            last_position = [float(num) for num in formatted_poslist[-1].split(',')]
        command = f'walk_by_points {poslist_str}'
        self.poco_gm(command)
        #移动完成判断（暂时先10s内判断）
        for i in range(10):
            current_position = self.get_current_position()
            if abs(last_position[0] - current_position[0]) <= 0.5 and abs(last_position[1] - current_position[1]) <= 0.5:
                print("已移动到目标位置")
                break
            elif i == 9:
                print('移动到死胡同，停止移动')
                stop_move_command = f'walk_by_points {",".join(str(num) for num in current_position)}'
                self.poco_gm(stop_move_command)
            else:
                print("移动中，请等待。。。")
                sleep(1.0)

    #向指定坐标移动
    def move_star(self,x,z):
        command = f'a_star {x} {z}'
        self.poco_gm(command)
        result = self.get_output().strip().split('\n')[-1]
        if result == 'success' :
            for i in range(10):
                current_position = self.get_current_position()
                if abs(x - current_position[0]) <= 1 and abs(z - current_position[1]) <= 1:
                    print("已移动到目标位置")
                    break
                else:
                    print("移动中，请等待。。。")
                    sleep(1.0)
        else:
            logger.info('目标点不可到达')
            for i in range(10):
                current_position_1 = self.get_current_position()
                self.sleep(1)
                current_position_2 = self.get_current_position()
                if abs(current_position_2[0] - current_position_1[0]) <= 0.5 and abs(current_position_2[1] - current_position_1[1]) <= 0.5:
                    print("已停止移动")
                    break
                else:
                    print("移动中，请等待。。。")
            



    #轮盘操作主角移动
    def move_stick(self,direction='W',duration=0.5):
        if self.poco_exists('joystick'):
            move_keywords = ["W","A","S","D"]
            vertexs = [(0.13,0.66),(0.07,0.77),(0.13,0.88),(0.19,0.77)]
            swipe_end = vertexs[move_keywords.index(direction)]
            origin = (0.13,0.77)
            platform = self.get_platform()
            if platform == 'Windows':
                self.long_press(direction,duration)
            elif platform == 'Android':
                self.swipe(origin,(swipe_end),duration)
             

    #拾取
    def pickup(self):
        if self.poco_exists('pickup'):
            self.poco_click("pickup")

    #砍树
    def cutdown(self):
        if self.poco_exists("ui://pkg_mainwindow/image/Main_icon_cutdown"):
            self.poco_click("ui://pkg_mainwindow/image/Main_icon_cutdown")

    #挖矿
    def mining(self):
        if self.poco_exists('ui://pkg_mainwindow/image/Main_icon_mining'):
            self.poco_click('ui://pkg_mainwindow/image/Main_icon_mining')

    #NPC对话
    def chat_with_npc(self):
        if self.poco_exists('ui://pkg_mainwindow/image/task_icon_11'):
            self.poco_click('ui://pkg_mainwindow/image/task_icon_11')

    #摇树
    def shake_tree(self):          
        if self.poco_exists('ui://pkg_mainwindow/image/Main_icon_shake'):
            self.poco_click('ui://pkg_mainwindow/image/Main_icon_shake')
    #收杆
    def fish(self):
        if self.poco_exists('ui://pkg_mainwindow/image/information_btn_01n'):
            self.poco_click('ui://pkg_mainwindow/image/information_btn_01n')

    #甩杆
    def fishing(self):
        if self.poco_exists('ui://pkg_mainwindow/image/Main_icon_finish'):
            self.poco_click('ui://pkg_mainwindow/image/Main_icon_finish')

    #使用（学习）
    def use(self):
        if self.poco_exists('ui://pkg_mainwindow/image/Main_icon_hand_01'):
            self.poco_click('ui://pkg_mainwindow/image/Main_icon_hand_01')

    #打开背包
    @BaseAirtest.handle_poco_timeout(retries=3, timeout=5)
    def open_backpack(self):
        if self.poco("rightsidebar").offspring(text='背包').exists():
            self.poco("rightsidebar").offspring(text='背包').click()
        elif self.poco_exists('ui://pkg_icon/image/gameuiicon/backpack/backpack_tab_icon_05n'):
            self.poco_click('ui://pkg_icon/image/gameuiicon/backpack/backpack_tab_icon_05n')
            self.sleep(1)
            
        
    #放置家具
    def place(self):
        if self.poco_exists('ui://pkg_mainwindow/image/Main_icon_place'):
            self.poco_click('ui://pkg_mainwindow/image/Main_icon_place')

    #打开手机
    @BaseAirtest.handle_poco_timeout(retries=3, timeout=5)
    def open_phone(self):
        if self.poco("rightsidebar").offspring(text='手机').exists():
            self.poco("rightsidebar").offspring(text='手机').click()

    #好友入口
    def open_friend(self):
        if self.poco_exists('ui://pkg_icon/image/gameuiicon/phone/friends_icon_45'):
            self.poco_click('ui://pkg_icon/image/gameuiicon/phone/friends_icon_45')

    #点击通讯录
    def friend_type(self):
        if self.poco_exists('ui://pe02mithvqx78ylx'):
            self.poco_click('ui://pe02mithvqx78ylx')
    
    #前往家园
    def tp_home(self):
        if self.poco_exists('brn_home'):
            self.poco_click('brn_home')
        elif self.poco_exists('ui://rbw1tvvvkkge43'):
            self.poco_click('ui://rbw1tvvvkkge43')
        elif self.poco_exists_bytext('前往家园'):
            self.poco_click_bytext('前往家园')
        home_flag = self.poco_exists_bytext('家园详情')
        while True:
            if home_flag:
                print('tp finish')
                break
            elif not self.poco_exists_bytext('前往家园') and not self.poco_exists('ui://pkg_mainwindow/image/Main_icon_hand_01'):
                print('传送中，请等待')
                self.sleep(1)
            elif self.poco_exists_bytext('尼克斯') or self.poco_exists_bytext('家园详情'):
                print('tp finish')
                break

    #返回按钮统一处理
    def back(self):
        if self.poco_exists('close'):
            self.poco_click('close')
        elif self.poco_exists('closeButton'):
            self.poco_click('closeButton')

    #领取奖励处理
    def claim_reward(self):
        if self.poco_exists_bytext('恭喜获得'):
            reward_name = self.poco('reward_item').offspring('text_name').get_text()
            reward_icon = self.poco('reward_item').offspring('item_icon').child().get_name()
            print(f'获得奖励:{reward_name}')
            logger.info(f'获得奖励:{reward_name}')
            print('icon:',reward_icon)
            self.poco_click_bytext('点击屏幕，界面关闭')
            return reward_name,reward_icon
    
    #GM频闭交互方向判断
    def operate_reinforce(self):
        self.poco_gm('operate_reinforce')
    
    #制造台制造（按钮）
    def making(self):
        if self.poco_exists('ui://pkg_mainwindow/image/house_icon_fabricate'):
            self.poco_click('ui://pkg_mainwindow/image/house_icon_fabricate')
        else:
            self.operate_reinforce()
            if self.poco_exists('ui://pkg_mainwindow/image/house_icon_fabricate'):
                self.poco_click('ui://pkg_mainwindow/image/house_icon_fabricate')
            else:
                raise Exception('There Is No Craft Station Nearby')
        
    #烹饪台制造（按钮）
    def cooking(self):
        if self.poco_exists('ui://pkg_mainwindow/image/house_icon_cooking'):
            self.poco_click('ui://pkg_mainwindow/image/house_icon_cooking')
        else:
            self.operate_reinforce()
            if self.poco_exists('ui://pkg_mainwindow/image/house_icon_cooking'): 
                self.poco_click('ui://pkg_mainwindow/image/house_icon_cooking')
            else:
                raise Exception('There Is No Cooking Station Nearby')
            
    #梳妆台（按钮）
    def dressing(self):
        if self.poco_exists('ui://pkg_mainwindow/image/house_icon_dressing'):
            self.poco_click('ui://pkg_mainwindow/image/house_icon_dressing')
        else:
            self.operate_reinforce()
            if self.poco_exists('ui://pkg_mainwindow/image/house_icon_dressing'):
                self.poco_click('ui://pkg_mainwindow/image/house_icon_dressing')
            else:
                raise Exception('There Is No Dress Station Nearby')
            
    #交互椅子等挂点家具
    def sit(self):
        if self.poco_exists('ui://pkg_mainwindow/image/house_icon_tap'):
            self.poco_click('ui://pkg_mainwindow/image/house_icon_tap')
        else:
            self.operate_reinforce()
            if self.poco_exists('ui://pkg_mainwindow/image/house_icon_tap'):
                self.poco_click('ui://pkg_mainwindow/image/house_icon_tap')
            else:
                raise Exception('There Is No Furniture Nearby')
            
    #通过物品id获取属性值(从templates中)
    def get_value_by_id(self,itemid,key):
        self.config = ConfigUtil()
        folder_path = self.config.get_yaml_value('resources.yaml','templates','path')
        folder = FolderQuery(folder_path)
        matching_values = folder.find_data('id', itemid, key)
        if not matching_values:
            # 如果没有匹配的值，尝试使用 'ID' 进行匹配
            matching_values = folder.find_data('ID', itemid, key)
        if matching_values:
            print(f"找到了与目标值 '{itemid}' 相关的{key}:")
            print(matching_values)
            if len(matching_values) > 1:
                return matching_values
            else:    
                return matching_values[0]
        else:
            print(f"未找到与目标值  '{itemid}' 相关的{key}.")
            return None
            
    #与阿太购买指定道具
    def buy_from_shota(self,itemid,num=1):
        self.move_to_npc_side('Shota')
        self.chat_with_npc()
        if self.poco_exists_bytext('商店服务'):
            self.poco_click_bytext('商店服务')
            goods_icon = self.get_value_by_id(itemid,'图标')
            goods_name = self.get_value_by_id(itemid,'名字_zh')
            scroll_times = 10
            while scroll_times > 0:
                goods = self.poco_exists(goods_icon)
                if goods:
                    try:
                        self.poco_click(goods_icon)
                        self.sleep(1)
                    except:
                        pass
                    if self.poco_exists_bytext(goods_name):
                        print('已选中目标商品')
                        self.poco_click_bytext('购买')
                        if num != 1:
                            self.poco_click('input_num')
                            for i in str(num):
                                self.poco_click(f"num{i}")
                            self.poco_click('sure')
                        self.poco_wait_click_text('确定')
                        self.sleep()
                        self.poco_wait_click_text('确定')
                        self.poco_wait_click_text('点击屏幕，界面关闭')
                        self.back()
                        self.poco_wait_click_text('感谢惠顾，欢迎常来！')
                        return
                self.swipe([0.8,0.6],[0.8,0.35])
                scroll_times -= 1
                self.sleep(1)

    #背包手持指定道具
    def hand_from_backpack(self,itemid):
        goods_icon = self.get_value_by_id(itemid,'图标')
        goods_name = self.get_value_by_id(itemid,'名字_zh')
        scroll_times = 10
        while scroll_times > 0:
            goods = self.poco_exists(goods_icon)
            if goods:
                try:
                    self.poco_click(goods_icon)
                    self.sleep(1)
                except:
                    pass
                if self.poco_exists_bytext(goods_name):
                    self.back()
                    return
            self.swipe([0.8,0.6],[0.8,0.35])
            scroll_times -= 1
            self.sleep(1)

    #制造台制造物品
    def make_by_craft_station(self,itemid,go_on=True):
        self.making()
        icon = self.get_value_by_id(itemid,'图标')
        name = self.get_value_by_id(itemid,'名字_zh')
        self.poco_click('ui://2r680p1zjqbl11')
        scroll_times = 3
        while scroll_times >= 0:
            goods = self.poco_exists(icon)
            if goods:
                try:
                    self.poco_click(icon)
                    self.sleep(1)
                except:
                    pass
                if self.poco(icon).parent().sibling('n8').exists():
                    self.poco_click_bytext('制造')
                    making_time = 10
                    while making_time >0:
                        if self.poco_exists_bytext("继续"):
                            if go_on:
                                self.poco_click_bytext("继续")
                            else:
                                self.poco_click_bytext("退出")
                            logger.info(f'{name}制造成功')
                            break

                        making_time -=1
                        self.sleep()
                    return
            elif scroll_times == 0:
                logger.info("无制造目标")
                if go_on:
                    pass
                else:
                    self.back()
                break
            self.swipe([0.8,0.6],[0.8,0.35])
            scroll_times -= 1
            self.sleep(1)



    #通过配方表获取对应制作材料
    def get_material(self,itemid):
        self.config = ConfigUtil()
        folder_path = self.config.get_yaml_value('resources.yaml','fabricate','path')
        folder = FolderQuery(folder_path)
        matching_values = folder.find_data('配方ID', itemid, "所需材料")
        if not matching_values:
            # 如果没有匹配的值，尝试使用 '物品ID' 进行匹配
            matching_values = folder.find_data('物品ID', itemid, "所需材料")
        
        matching_numbers = folder.find_data('配方ID', itemid, "材料数量")
        if not matching_numbers:
            # 如果没有匹配的值，尝试使用 '物品ID' 进行匹配
            matching_numbers = folder.find_data('物品ID', itemid, "材料数量")
        
        if matching_values and matching_numbers :
            values = [num for item in matching_values for num in item.split('|')]
            numbers = [num for item in matching_numbers for num in item.split('|')]
            for value,number in zip(values,numbers):
                logger.info(f"添加{value} {number}个")
                if value == '2':
                    self.add_money(gold_num=number)
                else:
                    self.add_backpack(value,number)

    #通过物品ID或配方ID获取配方（背包用的）
    def get_fabricate(self,itemid):
        self.config = ConfigUtil()
        folder_path = self.config.get_yaml_value('resources.yaml','fabricate','path')
        folder = FolderQuery(folder_path)
        matching_values = folder.find_data('配方ID', itemid, "配方ID")
        if not matching_values:
            # 如果没有匹配的值，尝试使用 '物品ID' 进行匹配
            matching_values = folder.find_data('物品ID', itemid, "配方ID")
        print(matching_values)
        if matching_values :
            if len(matching_values) > 1: 
                matching_values = matching_values
            else:    
                matching_values = matching_values[0]
            is_learn = folder.find_data('配方ID', matching_values, "默认学会(0:不会,99:草原,99:沙漠,99:都会)")
            is_learn = is_learn[0]
            folder_material_path = self.config.get_yaml_value('resources.yaml','templates','path')
            folder_material = FolderQuery(folder_material_path)
            matching_material = folder_material.find_data('解锁配方',matching_values,'id')
            if matching_material:
                if len(matching_material) >1 :
                    matching_material = matching_material
                else:
                    matching_material = matching_material[0]
                print(matching_material)
            else:
                matching_material = None
            return matching_material,is_learn



    #学习配方
    def learn_fabricate(self,itemid):
        icon = self.get_value_by_id(itemid,'图标')
        name = self.get_value_by_id(itemid,'名字_zh')
        self.add_backpack(itemid)
        self.open_backpack()
        self.poco_click(icon)
        self.back()
        self.sleep()
        self.use()


    #通过物品id学习配方
    def learn_by_goods(self,itemid):
        fabricate_id,is_learn = self.get_fabricate(itemid)
        print(fabricate_id,is_learn)
        if is_learn == '0' :
            self.learn_fabricate(fabricate_id)
        else:
            logger.info('该配方默认学会,无需再学')

        

        
        
            

    #装扮app预览指定装扮
    def preview_clothes(self,itemid):
        icon = self.get_value_by_id(itemid,'图标')
        part = self.get_value_by_id(itemid,'部位')
        name = self.get_value_by_id(itemid,'名字_zh')
        part_icon_list = {'1':'ui://pkg_icon/image/gameuiicon/avatar/clothing/login_icon_04n',
                          '2':'ui://pkg_icon/image/gameuiicon/avatar/clothing/login_tab_icon_5n',
                          '3':'ui://pkg_icon/image/gameuiicon/avatar/clothing/login_tab_icon_6n',
                          '4':'ui://pkg_icon/image/gameuiicon/avatar/clothing/login_tab_icon_8n',
                          '5':'ui://pkg_icon/image/gameuiicon/avatar/clothing/login_tab_icon_9n',
                          '6':'ui://pkg_icon/image/gameuiicon/avatar/clothing/login_tab_icon_10n',
                          '7':'ui://pkg_icon/image/gameuiicon/avatar/clothing/login_tab_icon_11n',
                          '8':'ui://pkg_icon/image/gameuiicon/avatar/clothing/Mapp_icon_18',
                          '9':'',
                          '11':'ui://pkg_icon/image/suit/Mapp_icon_20',
                          '12':'ui://pkg_icon/image/suit/Mapp_icon_21',
                          '13':'ui://pkg_icon/image/suit/login_icon_28',
                          '14':'ui://pkg_icon/image/gameuiicon/avatar/clothing/login_iconb_13n',
                          '15':'ui://pkg_icon/image/gameuiicon/avatar/clothing/backpack_icon_77',
                          '16':'ui://pkg_icon/image/gameuiicon/icon/appmall_icon_14n',
                          '17':'ui://pkg_icon/image/gameuiicon/avatar/clothing/login_iconb_15n',
                          '18':'ui://pkg_icon/image/gameuiicon/avatar/clothing/login_iconb_14n',
                          '19':'ui://pkg_icon/image/gameuiicon/avatar/clothing/backpack_icon_69',
                          '20':'ui://pkg_icon/image/gameuiicon/icon/appmall_icon_15n',
                          '21':'ui://pkg_icon/image/gameuiicon/avatar/clothing/login_iconb_16n',
                          '22':'ui://pkg_icon/image/gameuiicon/avatar/clothing/login_iconb_12n',
                          '24':''}
        clothing ='ui://pkg_icon/image/gameuiicon/avatar/outfit/dress_icon_09n'
        facial_features = 'ui://pkg_icon/image/gameuiicon/avatar/outfit/dress_icon_08n'
        apparel = 'ui://pkg_icon/image/gameuiicon/avatar/outfit/dress_icon_10n'
        skin = 'ui://pkg_icon/image/gameuiicon/avatar/clothing/login_icon_06n'
        clothing_part = ['11','12','13','14','15','16','17','18','19','20','21','22']
        facial_features_part = ['1','2','3','4','5','6','7','8']
        if part in clothing_part :
            self.poco_click(clothing)
            if self.poco_exists(part_icon_list[part]):
                self.poco_click(part_icon_list[part])
                if not self.poco(part_icon_list[part]).parent().sibling('n1').exists():
                    if clothing_part.index(part) < 6:
                        self.drag_to_position(part_icon_list['17'], [0.9, 0.9])
                    else:
                        self.drag_to_position(part_icon_list['16'], [0.2, 0.2])
                    self.sleep(1.0)
                    self.poco_click(part_icon_list[part])
            else:
                if clothing_part.index(part) < 6:
                    self.drag_to_position(part_icon_list['17'], [0.9, 0.9])
                else:
                    self.drag_to_position(part_icon_list['16'], [0.2, 0.2])
                self.sleep(1.0)
                self.poco_click(part_icon_list[part])
            scroll_times = 10
            while scroll_times > 0:
                goods = self.poco_exists(icon)
                if goods:
                    try:
                        self.poco_click(icon)
                        self.sleep(1)
                    except:
                        pass
                    if self.poco_exists_bytext(name) or self.poco(icon).parent().parent().parent().parent().offspring('n8').exists():
                        logger.info(f'已选中目标衣服{itemid}')
                        return
                if scroll_times < 7:
                    self.swipe([0.8,0.6],[0.8,0.35])
                else:
                    self.swipe([0.8,0.35],[0.8,0.6])
                scroll_times -= 1
                self.sleep(1)
        elif part in facial_features_part :
            self.poco_click(facial_features)
            if self.poco_exists(part_icon_list[part]):
                self.poco_click(part_icon_list[part])
                if not self.poco(part_icon_list[part]).parent().sibling('n1').exists():
                    if facial_features_part.index(part) < 6:
                        self.drag_to_position(part_icon_list['6'], [0.9, 0.9])
                    else:
                        self.drag_to_position(part_icon_list['6'], [0.2, 0.2])
                    self.sleep(1.0)
                    self.poco_click(part_icon_list[part])
            else:
                if facial_features_part.index(part) < 6:
                    self.drag_to_position(part_icon_list['6'], [0.9, 0.9])
                else:
                    self.drag_to_position(part_icon_list['6'], [0.2, 0.2])
                self.sleep(1.0)
                self.poco_click(part_icon_list[part])
            scroll_times = 10
            while scroll_times > 0:
                goods = self.poco_exists(icon)
                sprite = self.poco('n8')
                if goods:
                    try:
                        self.poco_click(icon)
                        self.sleep(1)
                    except:
                        pass
                    if self.poco(icon).parent().parent().parent().parent().offspring('n8').exists():
                        logger.info(f'已选中目标五官{itemid}')
                        return
                if scroll_times < 7:
                    self.swipe([0.8,0.6],[0.8,0.35])
                else:
                    self.swipe([0.8,0.35],[0.8,0.6])
                scroll_times -= 1
                self.sleep(1)
        elif part == '24':
            self.poco_click(skin)
            scroll_times = 10
            while scroll_times > 0:
                goods = self.poco_exists(icon)
                if goods:
                    try:
                        self.poco_click(icon)
                        self.sleep(1)
                    except:
                        pass
                    if self.poco_exists_bytext(name) or self.poco(icon).parent().parent().parent().parent().offspring('n8').exists():
                        logger.info(f'已选中目标皮肤{itemid}')
                        return
                if scroll_times < 7:
                    self.swipe([0.8,0.6],[0.8,0.35])
                else:
                    self.swipe([0.8,0.35],[0.8,0.6])
                scroll_times -= 1
                self.sleep(1)



        
    








            

    #GM添加物品
    def add_backpack(self,itemid,num=1):
        command = f'add_backpack {itemid} {num}'
        self.poco_gm(command)
        logger.info(f'已添加道具{itemid}')

    #GM添加通用
    def add_item(self,itemid,num=1):
        command = f'add_item {itemid} {num}'
        self.poco_gm(command)
        self.claim_reward()


    #GM清空背包
    def clean_backpack(self):
        self.poco_gm('clean_backpack')
        logger.info('背包已清空')
    
    #GM添加金币，钻石
    def add_money(self,diamond_num=0,gold_num=0,point=0):
        command = f'add_money {diamond_num} {gold_num} {point}'
        self.poco_gm(command)
        logger.info(f'已添加钻石{diamond_num} 金币{gold_num} 积分{point}')
        
        




    
    #移动到指定NPC处
    def move_to_npc_side(self,npc_name):
        self.config = ConfigUtil()
        npc_position = self.config.get_yaml_value('position.yaml','npc',npc_name)
        if npc_position != None:
            npc_position = [float(pos) for pos in npc_position.split(",")]
            self.move(npc_position)
        else:
            raise Exception('NPC Position Is None')

    #获取position.yaml文件中的坐标
    def get_yaml_position(self,section_name, obj_name):
        self.config = ConfigUtil()
        position = self.config.get_yaml_value('position.yaml',section_name, obj_name)
        if position != None:
            tuple_position = ast.literal_eval(position)
            return tuple_position
        else:
            return None
        


    #账号创建
    def sign_up(self,default=True):
        self.poco(text='这里是嗨放世界居民管理处，我是负责居民信息管理的小月。').wait(timeout=20).click()
        self.poco(text='正式成为嗨放世界的新居民前，请先填写居民登记表吧。').wait(timeout=5).click()
        self.poco(text='预设方案').wait(timeout=10)
        self.poco_click_bytext('下一步')
        self.poco(text='提交').wait(timeout=10)
        if default == True : 
            self.poco_click_bytext('提交')
        else:
            self.poco_click_bytext('沙漠风')
            self.sleep(1.0)
            self.poco_click_bytext('提交')
        self.poco(text='已收到并核实你的申请，恭喜您成为嗨放世界的新居民！马上将会送您进入您的专').wait(timeout=10).click()
        self.poco(text='旋转视角，找到公鸡').wait(timeout=15)



    #登录
    def login(self):
        #处理临时资源
        if self.poco_exists_bytext('临时界面, 后续删除'):
            self.poco_click_bytext("临时界面, 后续删除")
        login_time = 0
        while login_time < 60:
            #新号处理
            if self.poco_exists_bytext("游戏用户协议"):
                self.poco_click_bytext('全部同意')
                self.sleep(1.0)
                break
            #老号处理
            elif self.poco_exists_bytext('月份签到') or self.poco_exists_bytext('背包'):
                print('登录成功')
                self.back()
                break
            else:
                sleep(1.0)
            login_time += 1
    
    def start_game_now(self):
        self.start_game('com.mico.simsparty.wonderworld')
        self.sleep(5)
        self.login()

    #处理账号绑定拍脸弹窗
    def close_link_account(self):
        if self.poco_exists_bytext('账号绑定得好礼'):
            self.poco_click_bytext('今日内不再弹出')
            self.sleep(1)
            self.poco_click('ui://2ni11kbwk5web1')

    #界面引导处理（派对）
    def finish_interface_guide(self):
        if self.poco_exists('ui://1y6cq52pmh3ce'):
            while True:
                if self.poco_wait('ui://1y6cq52pmh3ce'):
                    self.poco_click('ui://1y6cq52pmh3ce')                
                if self.poco_wait('ui://2ni11kbwu65d8yji'):
                    self.poco_click('ui://2ni11kbwu65d8yji')
                    break
            


    #签到处理（签到当前可签到的天数n）
    def sing_in(self):
        if self.poco_exists_bytext('月份签到'):
            #获取当前签到天数
            signed_in_day = self.poco("day").get_text()
            today = str(int(signed_in_day) + 1).zfill(2)
            print(today)
            self.poco('day_list').offspring(text=today).click()
            if self.poco_wait_text('补签需要消耗'):
                self.poco_click('yes')
                self.claim_reward()
            else:
                self.claim_reward()
            

    #新手引导处理
    def rookie_guide(self):
        if not self.poco_exists_bytext('旋转视角，找到公鸡'):
            self.sleep(5.0)
        self.poco(text='旋转视角，找到公鸡').wait(timeout=15)
        self.swipe((0.6,0.6),(0.9,0.6))#转动视角
        self.poco(text='朝着').wait(timeout=5)
        if self.poco_exists_bytext('朝着'):
            self.swipe((0.1,0.7),(0.1,0.4),duration=1)#移动轮盘
            self.move_to_npc_side('rookie_Nicks')
            self.poco(text='初次见面，我是家园管家').wait(timeout=5).click()
            self.poco(text='放置在家园').wait(timeout=5).click()
            self.poco(text='点击屏幕，界面关闭').wait(timeout=5).click()
            self.poco(text='移动到指定地点').wait(timeout=5).click()
            self.move(((58.5,31.89),(65.9,32.40)))
            # self.poco("rightsidebar").offspring(text='背包').wait(timeout=5).click()#需要解决进不来
            self.open_backpack()
            self.poco("backapckbody").offspring(text='制造台').wait(timeout=5).click()
            self.poco(text='点击背包外任意地方退出背包').wait(timeout=5).click()
            self.poco(text='点击放置').wait(timeout=5)
            self.place()
            self.poco(text='很好。让我们来学习如何收集基础材料。首先请收集3个').wait(timeout=5).click()
            self.move(self.get_yaml_position('rookie_guide','Stone1'))
            self.pickup()
            self.move(self.get_yaml_position('rookie_guide','Stone2'))
            self.pickup()
            self.move(self.get_yaml_position('rookie_guide','Stone3'))
            self.pickup()
            self.poco(text='石头已经收集完成，下一步需要收集3个').wait(timeout=5).click()
            if self.poco_exists_bytext("移动到目标树木位置"):
                self.move(self.get_yaml_position('rookie_guide','Tree_shaking'))
                self.shake_tree()
                self.poco(text='拾取掉落的树枝。每棵树每天可摇晃三次。').wait(timeout=5)
                self.shake_tree()
                self.add_backpack(20100004,3)
                self.poco_wait_click_text("太棒了！你已经收集了足够的材料，现在去制造一把")
                self.poco(text='移动到制造台位置').wait(timeout=5)
                self.move(self.get_yaml_position('rookie_guide','back_Craft'))
                self.poco_wait_text('制造界面')
                self.making()
                self.poco('recipes').offspring('icon')[0].wait(timeout=5).click()
                self.sleep(1.0)
                self.poco_click_bytext('制造')
                self.poco(text='退出').wait(timeout=15).click()
                self.poco(text='不错。我们得到了一把石斧。试试使用它').wait(timeout=15).click()
                self.poco(text='移动到目标树木位置').wait(timeout=15)
                self.move(self.get_yaml_position('rookie_guide','Tree_cuting'))
                self.poco("rightsidebar").offspring(text='背包').wait(timeout=5).click()
                self.poco("backapckbody").offspring(text='石斧').wait(timeout=5).click()
                self.poco(text="点击背包外任意地方退出背包").wait(timeout=5).click()
                self.poco(text="砍树").wait(timeout=5)
                for i in range(3):
                    self.cutdown()
                    self.sleep(2.0)
                self.poco(text="非常好，你学会了伐木。砍树产出各种木材，木材是制").wait(timeout=5).click()    
                self.poco(text="阿太的").wait(timeout=5).click()
                self.poco(text="所处位置").wait(timeout=5)
                self.move(self.get_yaml_position('rookie_guide','back_Shota'))
                self.poco(text="进行对话").wait(timeout=5)
                self.chat_with_npc()
                self.poco(text="商店服务").wait(timeout=5).click()
                self.poco(text="点击选中").wait(timeout=5)
                self.poco_wait_click('ui://pkg_icon/image/tool/icon_pickaxe_rock')
                self.poco(text="石镐").wait(timeout=5)
                self.poco(text="购买").wait(timeout=5).click()    
                self.poco_wait_click_text("确定")
                self.poco_wait_click_text('点击屏幕，界面关闭')
                self.back()
                self.poco_wait_click_text('感谢惠顾，欢迎常来！')
                self.poco_wait_click_text('余的材料别忘了去阿太的家园商店出售换取金币哦。')
                self.poco_wait_text("移动到目标矿脉位置")
                self.move(self.get_yaml_position('rookie_guide','ore'))
                self.poco("rightsidebar").offspring(text='背包').wait(timeout=5).click()
                self.poco("backapckbody").offspring(text='石镐').wait(timeout=5).click()
                self.poco(text="点击背包外任意地方退出背包").wait(timeout=5).click()
                self.poco(text="每天每个矿脉可以挖矿5次").wait(timeout=5)
                for i in range(5):
                    self.mining()
                    self.sleep(2.0)
                self.poco(text="太棒了，你学会了挖矿。挖矿产出各种矿石，矿石是制").wait(timeout=5).click()  
                self.poco(text="他居民的家园参观。").wait(timeout=5).click()
                self.poco("btn_enter_homeland").offspring(text='随机拜访').wait(timeout=5).click()
                self.sleep(10)
                self.poco(text="逛逛小月的家园，并与小月对话").wait(timeout=5).click()
                self.move(self.get_yaml_position('rookie_guide','Luna'))
                self.poco(text="小月").wait(timeout=5).click()
                self.poco(text="手机功能强大，但最基础的当然还是用手机跟好朋友联").wait(timeout=5).click()
                self.poco(text="接受").wait(timeout=5).click()
                self.poco(text="现在我已经是你的好友啦，接着了解一下手机里的好友").wait(timeout=5).click()
                self.poco(text="在好友APP里可以看到你所有的好友，可以与他们进行").wait(timeout=5).click()
                self.poco("rightsidebar").offspring(text='手机').wait(timeout=5).click()
                self.open_friend()
                self.poco(text="这里可以搜索并添加好友，也可以直接向推荐好友发送").wait(timeout=5).click()
                for add_friend in self.poco("addfriendswidget").offspring(text='添加好友') :
                    try:
                        add_friend.click()
                    except:
                        pass
                self.friend_type()
                self.poco(text="通讯录显示了你所有的好友。哈哈，我是你在嗨放世界").wait(timeout=5).click()
                self.poco(text="在这里你可以前往拜访好友的家园小岛，也可以开始与").wait(timeout=5).click()
                self.poco_wait_click('ui://pe02mithvqx78ylw')
                self.poco_wait_click_text('我们是好朋友对吧，以后可别忘了经常跟我联系哦！')
                self.poco_click('closeButton')
                self.poco_wait_click_text('管家尼克斯好像正在找你呢？你可以先回去看看，我们')
                self.poco_wait_text('传送回家园')
                self.open_phone()
                self.tp_home()
                self.poco_wait_text('尼克斯')
                self.move_to_npc_side('rookie_Nicks')
                self.poco_wait_click_text('的指引下进一步了解嗨放世界。')
                self.poco_wait_text('这里显示的是当前追踪的主线任务。点击进入查看更多')
                self.poco_wait_click_text('成功钓鱼一次')
                self.poco_wait_click_text('这里显示的是当前章节的所有主线任务。')
                self.poco_wait_click_text('锁下一章节主线任务。')
                self.poco_wait_click_text('以追踪其他主线任务。')
                self.poco_wait_click_text('通过“帮助”的快捷入口可以查看相关攻略。')
                self.poco_wait_click_text('小岛会越来越漂亮和繁荣。')
                self.poco(text='点击屏幕，界面关闭').wait(timeout=5).click()
                self.back()

    #派对创建
    def start_party(self,patry_type:int=0,game=0):
        """    
        :param party_type= 0:chat 1:fashion 2:game 3:fireworks 4:birthday 5:music
        """
        self.open_phone()
        if self.poco_wait('ui://pkg_icon/image/gameuiicon/phone/party_icon_32'):
            self.poco_click('ui://pkg_icon/image/gameuiicon/phone/party_icon_32')
            self.sleep(1)
            if self.poco_exists('ui://1y6cq52pmh3ce'):
                self.finish_interface_guide()
            self.poco_wait_click_text('派对创建')
            self.poco_wait_text('举办！')
            patry_type_list = ['ui://p575d9oyjkvnm','ui://p575d9oyjkvnj','ui://p575d9oyjkvnh','ui://p575d9oyjkvnq','ui://p575d9oyjkvnl','ui://p575d9oyjkvnk']
            if patry_type > 3 :
                self.swipe([0.7,0.3],[0.5,0.3])
            self.poco_click(patry_type_list[patry_type])
            self.poco_click_bytext('举办！')
            if patry_type == 2 :
                self.poco_wait_text('选择游戏模式')
                if game != 0 :
                    self.poco_click_bytext('生存淘汰赛')
                    self.poco_click_bytext('确认')
                else:
                    self.poco_click_bytext('确认')
            loading_time = 0
            while loading_time < 20:
                party_start_flag = self.poco_exists_bytext('派对开始')
                if party_start_flag:
                    self.poco_click_bytext('派对开始')
                    self.finish_interface_guide()
                    logger.info('派对创建完成')
                    break
                else:
                    self.sleep(1)
                    logger.info("派对创建中，请等待...")

    #派对关闭
    def close_party(self):
        if self.poco_exists_bytext('关闭派对'):
            self.poco_click_bytext('关闭派对')
            self.poco_wait_text('是否关闭派对')
            self.poco_click_bytext('确认')
            self.poco_wait_text('派对结束')
            try:
                self.poco(textMatches='离开*').click()
            except:
                pass
            loading_time = 0
            while loading_time < 20:
                party_close_flag = self.poco_exists_bytext('随机拜访')
                if party_close_flag:
                    logger.info('派对关闭完成')
                    break
                else:
                    self.sleep(1)
                    logger.info("派对关闭中，请等待...")

    def stop_game_now(self):
        self.stop_game('com.mico.simsparty.wonderworld')


                
                 






                



                

                


        


   