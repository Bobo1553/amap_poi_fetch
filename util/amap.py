# coding:utf-8
# 高德地图：http://ditu.amap.com/  高德地图poi：http://lbs.amap.com/api/webservice/guide/api/search/#text


import json
import xlwt
from datetime import datetime
from urllib import request
from urllib.parse import quote

import time

from config.config import CONF


class AmapSpider(object):
    url_amap = None
    city_code = None
    types = None
    connect_char = None
    spider_count = 0

    def __init__(self, key, types, city_code, connect_char, polygon_or_text='text'):
        if polygon_or_text == 'text':
            self.url_amap = 'http://restapi.amap.com/v3/place/text?key={0}&types={1}&city={2}&citylimit=true&children=1&' \
                            'offset=20&page=pageindex&extensions=all'.format(key, types, city_code)
        else:
            self.url_amap = 'https://restapi.amap.com/v3/place/polygon?polygon={0},{1}|{2},{3}&key={4}&types={5}&' \
                            'children=1&offset=20&page=pageindex&extensions=all' \
                .format(city_code[0], city_code[1], city_code[2], city_code[3], key, types)
        self.city_code = city_code
        self.types = types
        self.connect_char = connect_char

    def get_data(self, page_index):
        # 暂停500毫秒，防止过快取不到数据
        time.sleep(0.5)
        print('今日爬取次数为{0}次'.format(AmapSpider.spider_count))
        if AmapSpider.spider_count >= CONF.count_threshold:
            exit(0)
        AmapSpider.spider_count += 1
        url = self.url_amap.replace('pageindex', str(page_index))
        print(url)
        # 中文编码
        url = quote(url, safe='/:?&=')
        with request.urlopen(url) as f:
            html = f.read()
        rr = json.loads(html)
        return rr['pois']

    def get_poi_data(self):
        total_count = 0
        print('获取城市为{0}，类型为{1}的POI数据开始'.format(self.city_code, self.types))

        with open(CONF.json_name, 'a') as f:
            for each_page in range(1, int(1000 / CONF.page_size * 2)):
                html = self.get_data(each_page)
                if not html:
                    break
                total_count += len(html)
                html = json.dumps(html).lstrip('[').rstrip(']')
                if each_page != 1:
                    html = "," + html
                else:
                    html = self.connect_char + html
                f.write(html)
        print('获取城市为{0}, 类型为{1}的POI数据结束, 数量为{2}'.format(self.city_code, self.types, total_count))
        return total_count

    # 写入数据到excel
    @staticmethod
    def write_data_to_excel(name):
        # 从文件中读取数据
        fp = open(CONF.json_name, 'r')
        result = json.loads(fp.read())
        # 实例化一个Workbook()对象(即excel文件)
        wbk = xlwt.Workbook()
        # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
        sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

        # 创建表头
        # for循环访问并获取数组下标enumerate函数
        for index, hkey in enumerate(CONF.hkeys):
            sheet.write(0, index, hkey)

        # 遍历result中的每个元素。
        for i in range(len(result)):
            offset = 0
            values = result[i]
            n = i + 1
            for index, key in enumerate(CONF.bkeys):
                val = ""
                # 判断是否存在属性key
                if key in values.keys():
                    val = values[key]
                if key == 'type':
                    val = val.split(';')
                    sheet.write(n, index + offset, val[0])
                    offset = 1
                    sheet.write(n, index + offset, val[1])
                    offset = 2
                    sheet.write(n, index + offset, ';'.join(val[2:]))
                elif key == 'location':
                    val = val.split(',')
                    sheet.write(n, index + offset, val[0])
                    offset = 3
                    sheet.write(n, index + offset, val[1])
                else:
                    sheet.write(n, index + offset, val)
        wbk.save(name + '.xls')
        print('保存到excel文件： ' + name + '.xls ！')

    @staticmethod
    def write_json_before():
        with open(CONF.json_name, 'w') as f:
            f.write('[')

    @staticmethod
    def write_json_after():
        with open(CONF.json_name, 'a') as f:
            f.write(']')

    @staticmethod
    def write_json_spliter():
        with open(CONF.json_name, 'a') as f:
            f.write(',')


if __name__ == '__main__':
    CONF.parse_from_file('../config.yml')
    amap_spider = AmapSpider(CONF.key, CONF.types[0], '110107')
    # amap_spider.get_poi_data()
    amap_spider.write_data_to_excel('../data/{0}'.format('110107'))
