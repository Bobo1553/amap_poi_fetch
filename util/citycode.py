# coding=utf-8

import xlrd
from xlutils.copy import copy


class CityCode(object):
    finish_city = None
    city_code = None
    workbook = None
    write_book = None
    finish_index = None

    def __init__(self):
        self.finish_city = []
        self.city_code = []
        # 第一页为说明情况
        # 第二页为高德所提供的城市的API
        # 第三页为目前已经爬取完成的城市的API
        # 第四页为可能存在的错误信息
        self.workbook = xlrd.open_workbook('AMap_API_Table/高德地图API 城市编码对照表.xls')

        # 初始化
        self.init_finish_city()
        self.init_city_code()

        self.write_book = copy(self.workbook)

    def init_city_code(self):
        # 根据sheet索引或者名称获取sheet内容
        city_info = self.workbook.sheet_by_index(1)  # sheet索引从0开始

        # 获取整行和整列的值（数组）
        self.city_code = city_info.col_values(1)[1:]  # 获取第三列内容

    def init_finish_city(self):
        # 根据sheet索引或者名称获取sheet内容
        city_info = self.workbook.sheet_by_index(2)  # sheet索引从0开始

        # 获取整行和整列的值（数组）
        self.finish_city = city_info.col_values(0)[1:]  # 获取第三列内容

        self.finish_index = len(self.finish_city) + 1

    def fetch_city_code_for_spider(self):
        filter_result = [col for col in self.city_code if not col.endswith('00') and col not in self.finish_city]
        return filter_result

    def write_finish_city_code(self, city_code, spider_type, count):
        finish_sheet = self.write_book.get_sheet(2)
        finish_sheet.write(self.finish_index, 0, city_code)
        finish_sheet.write(self.finish_index, 1, spider_type)
        finish_sheet.write(self.finish_index, 2, count)
        self.finish_index += 1

    def save(self):
        self.write_book.save('AMap_API_Table/高德地图API 城市编码对照表.xls')


if __name__ == '__main__':
    city_code_item = CityCode()
    city_code_item.write_finish_city_code('11111', '110101', 555)
    city_code_item.save()
    # print(CityCode().fetch_city_code_for_spider())
