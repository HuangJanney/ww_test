import xlrd,xlwt
from utils.file_util import FileUtil
import pandas as pd
from xlwt import Workbook
from PIL import Image
import os
import csv
import chardet

class ExcelReader(object):

    def __init__(self, excel_name, sheet_name=None):
        excel_path = FileUtil.get_full_path(excel_name)
        self.data = xlrd.open_workbook(excel_path)
        self.__init_table_value(sheet_name)

    def get_rows_values(self, start_row=0, end_row=None):
        end_row = self.table.nrows - 1 if end_row is None else end_row
        rows_values = []
        for row_idx in range(start_row, end_row + 1):
            row_values = self.table.row_values(row_idx)
            rows_values.append(row_values)
        return rows_values

    def get_col_index(self, col_title):
        first_row_values = self.table.row_values(0)
        col_nums = len(first_row_values)
        for col_index in range(0, col_nums):
            if col_title == first_row_values[col_index]:
                return col_index
        return -1
    

    def get_column_values(self, col, start_row=0, end_row=None):
        """
        获取指定列的数据。

        参数：
        - col_index: 列索引。
        - start_row: 起始行索引（默认为0）。
        - end_row: 结束行索引（默认为None，表示最后一行）。

        返回一个包含指定列数据的列表。

        """
        if isinstance(col, str):  # 如果col是字符串
            col_index = self.get_col_index(col)  # 获取列索引
        # 如果col是整数，则直接使用传入的值
        else:
            col_index = col
        end_row = self.table.nrows - 1 if end_row is None else end_row
        column_values = []
        for row_idx in range(start_row, end_row + 1):
            cell_value = self.table.cell_value(row_idx, col_index)
            column_values.append(cell_value)
        return column_values

    def __init_table_value(self, sheet_name):
        # 未指定sheet_name时，默认取第一个sheet
        if sheet_name is None:
            self.table = self.data.sheet_by_index(0)
        else:
            self.table = self.data.sheet_by_name(sheet_name)



class ExcelWrite(object):
    def __init__(self, excel_name, sheet_name='Sheet1'):
        self.workbook = Workbook()
        self.excel_name = excel_name 
        self.sheet = self.workbook.add_sheet(sheet_name)

    def write_excel(self,row ,col ,value):
        if isinstance(value, str):
            self.sheet.write(row, col, value)
        elif isinstance(value, Image.Image):
            drawing = self.workbook.add_drawing()
            drawing.picture.data = value.tobytes()
            drawing.set_position(row, col)
            self.sheet.insert_bitmap_image(drawing)
    
    def save_excel(self):
        self.workbook.save(self.excel_name)









class CsvReader(object):
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)

    def get_row(self, row_index):
        return self.df.iloc[row_index]

    def get_col(self, col_index):  
        return self.df.iloc[:, col_index]

    def get_value(self, row_index, col_index):
        return self.df.iloc[row_index, col_index]
    


class FolderQuery(object):

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def find_data(self, target_column, target_value, return_column):
        matching_values = []

        def search_csv_files(folder_path):
            for root, _, files in os.walk(folder_path):
                for filename in files:
                    if filename.endswith('.csv'):
                        file_path = os.path.join(root, filename)
                        detected_encoding = chardet.detect(open(file_path, 'rb').read())['encoding']

                        if detected_encoding is not None:
                            with open(file_path, 'r', encoding=detected_encoding, errors='ignore') as file:
                                csv_reader = csv.DictReader(file)

                                for row in csv_reader:
                                    # if target_column in row and target_value in row[target_column] and return_column in row:#模糊匹配
                                    if target_column in row and row[target_column] == target_value and return_column in row:
                                        matching_values.append(row[return_column])

                        else:
                            print(f"无法确定文件 {file_path} 的编码")

        search_csv_files(self.folder_path)

        # 返回查找结果
        if matching_values:
            return matching_values
        else:
            return None


