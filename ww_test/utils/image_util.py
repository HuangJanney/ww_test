import os
from PIL import Image
from PIL import ImageChops
import math
import operator
from functools import reduce

from utils.file_util import FileUtil


class ImageUtil(object):

    @classmethod
    def merge(cls, original_img_path, background_img_path):
        """
        将原图和背景图进行合并
        :param original_img_path: 原图的绝对路径
        :param background_img_path: 背景图的绝对路径
        :return: 合并后的图片（Image对象）
        """
        org_img = Image.open(original_img_path)
        bgd_img = Image.open(background_img_path)

        org_img_width, org_img_height = org_img.size
        bgd_img_width, bgd_img_height = bgd_img.size

        # 先将原图处理成与背景图等宽
        org_img = org_img.resize((bgd_img_width, int(bgd_img_width / org_img_width * org_img_height)), Image.ANTIALIAS)

        # 将原图粘贴于背景图中央位置
        bands = org_img.split()
        mask = bands[3] if len(bands) > 3 else None
        bgd_img.paste(org_img, (0, bgd_img_height - org_img_height), mask=mask)

        bgd_img = bgd_img.resize((300, 350), Image.ANTIALIAS)

        return bgd_img

    @classmethod
    def crop(cls, org_img, scale_box):
        """
        对图片进行裁剪
        :param org_img: 原始图片（Image对象）
        :param scale_box: 左/上/右/下的裁剪比例
        :return: 裁剪后的图片（Image对象）
        """
        width, height = org_img.size
        box = (width * scale_box[0], height * scale_box[1], width * scale_box[2], height * scale_box[3])
        crop_img = org_img.crop(box)
        return crop_img

    @classmethod
    def save_file(cls, img, path):
        img.save(path)

    @classmethod
    def process_costume_pic(cls):
        """
        处理服饰图片（合并背景+裁剪）
        """
        org_img_dir = FileUtil.get_img_path('warehouse', 'driver', 'costume_org')
        dest_img_dir = FileUtil.get_img_path('warehouse', 'driver', 'costume')
        scale_box = (0.2, 0.3, 0.8, 0.8)
        cls.__process_pic(org_img_dir, dest_img_dir, scale_box)

    @classmethod
    def process_skidmark_pic(cls):
        """
        处理胎印图片（合并背景+裁剪）
        """
        org_img_dir = FileUtil.get_img_path('warehouse', 'racing_car', 'car_decoration_org', 'skidmark')
        dest_img_dir = FileUtil.get_img_path('warehouse', 'racing_car', 'car_decoration', 'skidmark')
        scale_box = (0.2, 0.3, 0.8, 0.8)
        cls.__process_pic(org_img_dir, dest_img_dir, scale_box)

    @classmethod
    def process_license_pic(cls):
        """
        处理车牌图片（合并背景+裁剪）
        """
        org_img_dir = FileUtil.get_img_path('warehouse', 'racing_car', 'car_decoration_org', 'licence')
        dest_img_dir = FileUtil.get_img_path('warehouse', 'racing_car', 'car_decoration', 'licence')
        scale_box = (0.1, 0.35, 0.9, 0.7)
        cls.__process_pic(org_img_dir, dest_img_dir, scale_box)

    @classmethod
    def __process_pic(cls, org_img_dir, dest_img_dir, scale_box):
        """
        对目标路径下的图片进行合并背景并做裁剪
        :param org_img_dir: 原始图片路径
        :param dest_img_dir: 处理后的图片存储路径
        :param scale_box: 左/上/右/下的裁剪比例
        """
        if os.path.exists(org_img_dir):
            FileUtil.recreate_dir(dest_img_dir)
            back_img_path = FileUtil.get_img_path('warehouse', 'driver', 'item_background.png')
            for root, dirs, files in os.walk(org_img_dir):
                for file in files:
                    org_img_path = os.path.join(root, file)
                    dest_img_path = os.path.join(dest_img_dir, file)
                    dest_img = cls.merge(org_img_path, back_img_path)
                    dest_img = cls.crop(dest_img, scale_box)
                    cls.save_file(dest_img, dest_img_path)
            # FileUtil.remove_dir(org_img_dir)

    @classmethod
    def compare_images(cls, org_img_path, cmp_img_path, diff_img_path):
        """
        比较图片，如果有不同则生成展示不同的图片
        @param: org_image_path: 原始图的路径
        @param: cmp_image_path: 对比图的路径
        @param: diff_image_path: 差异图的保存路径
        """
        org_image = Image.open(org_img_path)
        cmp_image = Image.open(cmp_img_path)
        try:
            diff = ImageChops.difference(org_image, cmp_image)
            if diff.getbbox() is None:
                print("same")
            else:
                diff.save(diff_img_path)
        except ValueError as e:
            print(e)

    @classmethod
    def image_contrast(cls, org_img_path, cmp_img_path):
        image1 = Image.open(org_img_path)
        image2 = Image.open(cmp_img_path)
        # 计算两张图片的直方图
        h1 = image1.histogram()
        h2 = image2.histogram()
        # 计算欧氏距离，表示对比度
        result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
        return result
    

    @classmethod
    def merge_images(cls, original_img_path, background_img_path,output_path):
        """
        将原图和背景图进行合并
        :param original_img_path: 原图的绝对路径
        :param background_img_path: 背景图的绝对路径
        :return: 合并后的图片（Image对象）
        """
        org_img = Image.open(original_img_path)
        bgd_img = Image.open(background_img_path)

        org_img_width, org_img_height = org_img.size
        bgd_img_width, bgd_img_height = bgd_img.size
        # 计算覆盖图在背景图中居中的位置
        x_position = (bgd_img_width - org_img_width) // 2
        y_position = (bgd_img_height - org_img_height) // 2



        # 将原图粘贴于背景图中央位置
        bgd_img.paste(org_img, (x_position,y_position),org_img)

        bgd_img.save(output_path)



if __name__ == '__main__':
    ImageUtil.process_costume_pic()
    ImageUtil.process_skidmark_pic()
    ImageUtil.process_license_pic()
