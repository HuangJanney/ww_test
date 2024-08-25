from utils.log_util import logger
import traceback
from airtest.core.api import *
from utils.file_util import FileUtil
from utils.config_util import ConfigUtil
from airtest.aircv import *
import pyautogui
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import requests
import json
from poco.drivers.std import StdPoco
from poco.utils.simplerpc.simplerpc import RpcTimeoutError
import poco.exceptions
from PIL import Image


# from src.util.config_util import ConfigReader

# from subprocess import check_output
# ST.OPDELAY = 2
# auto_setup(__file__)

class BaseAirtest(object):
    '''将airtest的一些基础操作函数简化，以便可以脱离airtestIDE'''

    def __init__(self):
        self.device = device()
        # self.device = connect_device('Android:///')
        # self.screen_width = self.device.display_info["height"]
        # self.screen_height = self.device.display_info["width"]
        self.poco = StdPoco()


    #依据device配置设置初始化连接
    def set_device(self,device='device'):
        config_util = ConfigUtil()
        config = config_util.read_yaml('device.yaml')
        # 遍历配置文件中的设备信息
        device_info = config['device']
        platform = device_info['platform']
        device_id = device_info['deviceId']
        # 根据平台初始化设备连接
        try:
            if platform == 'Android':
                if device_id == '':
                    return connect_device('Android:///')
                else:
                    return connect_device(f"Android:///{device_id}")
            elif platform == 'Windows':
                return connect_device(f"Windows:///?title_re={device_id}")
        except Exception as e:
            print(f"设备连接错误: {str(e)}")

    #获取当前配置的设备类型
    def get_platform(self):
        config_util = ConfigUtil()
        config = config_util.read_yaml('device.yaml')
        # 遍历配置文件中的设备信息
        device_info = config['device']
        platform = device_info['platform']
        return platform
    
    #获取当前配置的设备ID或窗口标题
    def get_device_id(self):
        config_util = ConfigUtil()
        config = config_util.read_yaml('device.yaml')
        # 遍历配置文件中的设备信息
        device_info = config['device']
        device_id = device_info['deviceId']
        return device_id



    def preview_item(self):
        self.controller.swipe([0.5, 0.5], [0.9, 0.6])
        self.controller.swipe([0.5, 0.5], [0.9, 0.6])

    def touch_coordinate(self, scale_x, scale_y):
        coord = self.__tans_to_coord(scale_x, scale_y)
        touch(coord)

    #融合PC端窗口坐标计算（2023.10.14更新）
    def __tans_to_coord(self, scale_x, scale_y):
        platform = self.get_platform()
        if platform == 'Android':
            coord_x = scale_x * self.screen_width
            coord_y = scale_y * self.screen_height
            coord = [coord_x, coord_y]
            return coord
        elif platform == 'Windows':
            left,top = self.get_window_origin()
            coord_x = (scale_x * self.screen_width) + left
            coord_y = (scale_y * self.screen_height) + top
            coord = [coord_x, coord_y]
            return coord
    

    def swipe(self, tuple_from_xy, tuple_to_xy, duration=0.5, steps=5):
        from_x = tuple_from_xy[0]
        from_y = tuple_from_xy[1]
        to_x = tuple_to_xy[0]
        to_y = tuple_to_xy[1]
        v1 = self.__tans_to_coord(from_x, from_y)
        v2 = self.__tans_to_coord(to_x, to_y)
        swipe(v1, v2, duration=duration, steps=steps)

    def touch_coord(self,scale_x, scale_y):
        coord = [scale_x, scale_y]
        touch(coord)

    # 向上滑动屏幕右侧
    def scroll_tab_up(self):
        self.swipe([0.8, 0.6], [0.8, 0.2])

    @classmethod
    def get_icon_path(cls, *icon_path):
        return FileUtil.get_img_path(*icon_path)
    
    @classmethod
    def get_snapshot_path(cls, filename,*snapshot_path):
        return FileUtil.get_snapshot_path(filename,*snapshot_path)

    @classmethod
    def sleep(cls, secs=1.0):
        sleep(secs=secs)

    @classmethod
    def exists_diy(cls, filename, threshold=0.7):
        return exists(Template(filename, threshold=threshold))

    @classmethod
    def exists_recursively(cls, threshold=0.7, *recursive_path):
        filename = cls.get_icon_path(*recursive_path)
        return cls.exists_diy(filename, threshold=threshold)

    @classmethod
    def exists_recursively_default(cls, *recursive_path):
        return cls.exists_recursively(0.7, *recursive_path)

    @classmethod
    def touch(cls, filename, threshold=0.7):
        touch(Template(filename, threshold=threshold))

    @classmethod
    def touch_recursively(cls, threshold=0.6, *recursive_path):
        filename = cls.get_icon_path(*recursive_path)
        logger.info('touch pic: %s' % filename)
        try:
            cls.touch(filename, threshold=threshold)
        except TargetNotFoundError:
            logger.error(traceback.format_exc())
            # subprocess.call('pause', shell=True)

    @classmethod
    def touch_recursively_default(cls, *recursive_path):
        cls.touch_recursively(0.6, *recursive_path)
        sleep()

    @classmethod
    def press_and_lold(cls, duration=2.0, *recursive_path):
        filename = cls.get_icon_path(*recursive_path)
        touch(Template(filename, duration=duration))

    @classmethod
    def assert_exists(cls, filename, threshold=0.7):
        return assert_exists(Template(filename, threshold=threshold))

    @classmethod
    def assert_exists_recursively(cls, threshold=0.6, *recursive_path):
        filename = cls.get_icon_path(*recursive_path)
        return cls.assert_exists(filename, threshold=threshold)

    @classmethod
    def assert_exists_recursively_default(cls, *recursive_path):
        return cls.assert_exists_recursively(0.6, *recursive_path)

    @classmethod
    def wait(cls, filename, threshold=0.7):
        return wait(Template(filename, threshold=threshold))

    @classmethod
    def wait_recursively(cls, threshold=0.6, *recursive_path):
        filename = cls.get_icon_path(*recursive_path)
        return cls.wait(filename, threshold=threshold)

    @classmethod
    def wait_recursively_default(cls, *recursive_path):
        return cls.wait_recursively(0.7, *recursive_path)

    #截图，并存储至results\snapshot下
    @classmethod
    def snapshot_img(cls,filename,*recursive_path):
        filename_path = cls.get_snapshot_path(filename,*recursive_path)
        snapshot(filename_path)
        cls.sleep()
        return filename_path

    def start_recording(self):
        logger.debug('start recording')
        self.device.start_recording()

    def stop_recording(self, filename='result.mp4', *subdir):
        save_path = FileUtil.get_video_path(filename, *subdir)
        logger.debug('stop recording, video save_path = %s' % save_path)
        self.device.stop_recording(output=save_path)
        
    #设置text图片
    @classmethod
    def create_image_by_text(cls,text,font_size, output_image_path):
        font_path = FileUtil.get_font_path('FangZhengHeiTiJianTi-1.ttf')
        # font = ImageFont.truetype(font_path, font_size)
        # image = Image.new("RGB", (1, 1), (255, 255, 255))
        # draw = ImageDraw.Draw(image)
        # text_width, text_height = draw.textsize(text, font=font)
        # image = Image.new("RGB", (text_width + 10, text_height + 10), (255, 255, 255))
        # draw = ImageDraw.Draw(image)
        # draw.text((5, 5), text, fill=(0, 0, 0), font=font)
        # image = image.resize((text_width + 20, text_height + 20), Image.ANTIALIAS)
        # image.save(output_image_path, quality=95)
        font = ImageFont.truetype(font_path, font_size)
        image = Image.new("RGB", (1, 1), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        text_width, text_height = draw.textsize(text, font=font)
        image = Image.new("RGB", (text_width, text_height), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, fill=(0, 0, 0), font=font)
        image.save(output_image_path, quality=95) 

    #通过文字进行点击操作(有效率很低，暂不使用)
    @classmethod
    def touch_by_text(cls,text):
        text_img_path = cls.get_icon_path('text_img','temp.png')
        cls.create_image_by_text(text,42,text_img_path)
        cls.sleep(3.0)
        cls.touch_recursively_default(text_img_path)
    
    #Android端删除输入框字符
    @classmethod
    def del_text(cls,num):
        for i in range(num):
            keyevent("67")
            if i == num:
                print("已删除完成")

                
    #Windows端按按键
    @classmethod
    def key_press(cls,keyword):
        pyautogui.press(keyword)

    #Windows端长按
    @classmethod
    def long_press(cls,keyword,duration:int=1):
        pyautogui.keyDown(keyword)
        cls.sleep(duration)
        pyautogui.keyUp(keyword)

    #将图片转换为文字（默认中文）
    @classmethod
    def img_to_string(cls,file_path,lang='chi_sim'):
        img = Image.open(file_path)
        string_result = pytesseract.image_to_string(img,lang)
        string_result = string_result.replace(' ','')#去除多余的空格
        return string_result
    
    #发送基础的post请求消息（用于飞书机器人）
    @classmethod
    def send_message(cls,url,message_text):
        message = {
                    "msg_type": "text",
                    "content": {
                        "text": message_text 
                                }
                    }
        message_json = json.dumps(message)
        response = requests.post(url, data=message_json, headers={"Content-Type": "application/json"})
        # 检查响应
        if response.status_code == 200:
            print("Message sent successfully")
        else:
            print("Message sending failed with status code:", response.status_code)
            print(response.text)

    #裁剪图片
    @classmethod
    def cut_img(cls,file_path,left,top,right,bottom,img_name="cut_img.png", *subdir):
        """    
        :param file_path : 图片路径
        :param left : 左上角 x 坐标
        :param top : 左上角 y 坐标
        :param right  : 右下角 x 坐标
        :param bottom  : 右下角 y 坐标
        :param img_path : 裁剪之后的图片
        """
        img = Image.open(file_path)
        #指定截图区域
        left = left  # 左上角 x 坐标
        top = top   # 左上角 y 坐标
        right = right  # 右下角 x 坐标
        bottom = bottom  # 右下角 y 坐标
        cropped_image = img.crop((left, top, right, bottom))
        # 保存截取的部分为新的图片
        img_path = FileUtil.get_snapshot_path(img_name, *subdir)
        cropped_image.save(img_path)
        cls.sleep(5.0)
        return img_path

    #Windows端输入文字
    @classmethod
    def input_world(cls,text):
        for word in text:
            if word ==' ':
                pyautogui.press('space')
            else:
                pyautogui.typewrite(text)

    #windows端删除输入框字符
    @classmethod
    def backspace_press(cls,num):
        for i in range(num):
            pyautogui.press("backspace")
            if i == num:
                print("已删除完成")

    # 启动游戏
    def start_game(self, packbag_name):
        packbag_name = 'com.mico.simsparty.wonderworld'
        start_app(packbag_name)

    # 关闭游戏
    def stop_game(self,packbag_name):
        stop_app(packbag_name)

    # 初始化输入文字
    @classmethod
    def text_phone(cls, words,enter=False):
        # start_app('com.netease.nie.yosemite')
        text(words,enter=False)

    # home操作
    @classmethod
    def home_phone(cls):
        home()

    # back操作
    @classmethod
    def back_phone(cls):
        keyevent("BACK")

    #输入文字合并
    def input_text(self,text):
        platform = self.get_platform()
        try:
            if platform == 'Android':
                self.text_phone(text)
            elif platform == 'Windows':
                self.input_world(text)
        except Exception as e:
            print(f"输入错误: {str(e)}")

    #删除文字合并
    def delete_text(self,length:int=1):
        platform = self.get_platform()
        try:
            if platform == 'Android':
                self.del_text(length)
            elif platform == 'Windows':
                self.backspace_press(length)
        except Exception as e:
            print(f"删除错误: {str(e)}")

    #获取屏幕分辨率（宽度）
    def get_screen_width(self):
        platform = self.get_platform()
        self.device = self.set_device()
        try:
            if platform == 'Android':
                screen_width = self.device.display_info["height"]
                screen_height = self.device.display_info["width"]
                return screen_width , screen_height
            elif platform == 'Windows':
                import pygetwindow as gw
                device_id = self.get_device_id()
                window = gw.getWindowsWithTitle(device_id)[0]
                screen_width = window.width
                screen_height  =  window.height
                return screen_width , screen_height
        except Exception as e:
            print(f"获取分辨率出错: {str(e)}")

    #获取Windows窗口的位置顶点（左边界、上边界）
    def get_window_origin(self):
        import pygetwindow as gw
        device_id = self.get_device_id()
        window = gw.getWindowsWithTitle(device_id)[0]
        left = window.left
        top  =  window.top
        return left , top


    @classmethod
    def adb_shell(cls,cmd):
        return shell(cmd)
    
    def handle_poco_timeout(retries=3, timeout=10):
        def decorator(func):
            def wrapper(*args, **kwargs):
                retry_count = 0
                current_timeout = timeout  # 使用 current_timeout 保存 timeout 的值
                while retry_count < retries:
                    try:
                        return func(*args, **kwargs)
                    except RpcTimeoutError:
                        retry_count += 1
                        print(f"Poco query timed out. Retrying... (Attempt {retry_count})")
                        current_timeout *= 2  # 使用 current_timeout
                        time.sleep(1)
                    except poco.exceptions.PocoNoSuchNodeException as e:
                        print("Encountered PocoNoSuchNodeException. Retrying in {} seconds...".format(current_timeout))
                        time.sleep(current_timeout)
                        retry_count += 1
                        current_timeout *= 2
                print("Poco query failed after maximum retries.")
                return None
            return wrapper
        return decorator

    @handle_poco_timeout(retries=3, timeout=5)
    def poco_click(self,query):
        element = self.poco(query)
        element.click()

    @handle_poco_timeout(retries=3, timeout=5)
    def poco_click_bytext(self,texts):
        self.poco(text=texts).click()

    @handle_poco_timeout(retries=3, timeout=5)
    def poco_set_text(self,query,text):
        element = self.poco(query)
        element.set_text(text)

    @handle_poco_timeout(retries=3, timeout=5)
    def poco_get_text(self,query):
        element = self.poco(query)
        return element.get_text()
    
    @handle_poco_timeout(retries=3, timeout=5)
    def poco_exists(self,query):
        element = self.poco(query)
        return element.exists()
    

    @handle_poco_timeout(retries=3, timeout=5)
    def poco_exists_bytext(self,texts):
        return self.poco(text=texts).exists()

    @handle_poco_timeout(retries=3, timeout=5)
    def poco_wait(self,query):
        element = self.poco(query)
        return element.wait(timeout=20)
    
    @handle_poco_timeout(retries=3, timeout=5)
    def poco_wait_text(self,text):
        element = self.poco(text=text)
        return element.wait(timeout=20)
    
    @handle_poco_timeout(retries=3, timeout=5)
    def poco_wait_click(self,query):
        element = self.poco(query)
        element.wait(timeout=20).click()

    @handle_poco_timeout(retries=3, timeout=5)
    def poco_wait_click_text(self,text):
        element = self.poco(text=text)
        element.wait(timeout=20).click()




    @handle_poco_timeout(retries=3, timeout=5)
    def poco_gm(self,cmd):
        self.poco("root_scene").set_text(f"gm {cmd}")
    
    #清除GM输出
    def clean_output(self):
        self.poco_gm('clean_output')
        self.sleep(1.0)

    #获取GM输出
    @handle_poco_timeout(retries=3, timeout=5)
    def get_output(self):
        output = self.poco("root_scene").get_text()
        return output
    
    #通过GM查询参数
    def select_by_gm(self,cmd):
        self.clean_output()
        self.poco_gm(cmd)
        self.sleep(3.0)
        value = self.get_output()
        return value
    

    #poco控件拖动到另一个控件
    @handle_poco_timeout(retries=3, timeout=5)
    def drag_to_other(self,query1,query2):
        self.poco(query1).drag_to(self.poco(query2))

    #poco控件拖动到坐标位置
    @handle_poco_timeout(retries=3, timeout=5)
    def drag_to_position(self,query,position):
        self.poco(query).drag_to(position)

    

    #通过poco获取屏幕元素图片
    def capture_poco(self,query,save_name,*recursive_path):
        # 使用 Poco 定位图像
        element = self.poco(query)

        # 获取图像的位置和大小
        icon_position = element.attr("pos")
        icon_size = element.attr("size")

        # 使用图像位置和大小截取屏幕图像
        screen_image = self.snapshot_img(save_name,*recursive_path)
        icon_image = self.cut_img(screen_image,icon_position[0]*self.screen_width, (icon_position[1]-icon_size[1])*self.screen_height, (icon_position[0] + icon_size[0])*self.screen_width, (icon_position[1])*self.screen_height,save_name,*recursive_path)

        # 返回截取到的图像对象
        return icon_image



