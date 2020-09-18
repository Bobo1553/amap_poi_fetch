# coding=utf-8
# author=Yijia Xiao
from config.config import CONF
from util.amap import AmapSpider
from util.citycode import CityCode


def download_each_city(city_code):
    connect_char = ''
    AmapSpider.write_json_before()
    hospital_count = 0
    for spider_type in CONF.types:
        if hospital_count != 0:
            connect_char = ','
        amap_spider = AmapSpider(CONF.key, spider_type, city_code, connect_char)
        hospital_count = amap_spider.get_poi_data()
    AmapSpider.write_json_after()
    AmapSpider.write_data_to_excel('temp_data3/{0}'.format(str(city_code)))


def down_load_data():
    # 解析配置文件
    CONF.parse_from_file('config/config.yml')
    print(CONF.key)

    # 南京市
    city_codes = ['320102', '320104', '320105', '320106', '320111', '320113', '320114', '320115', '320116', '320117', '320118']
    # 合肥市
    # city_codes = ['340102','340103','340104','340111','340121','340122','340123','340124','340181']
    # 徐州市
    # city_codes = ['320302','320303','320305','320311','320312','320321','320322','320324','320381','320382']
    # 苏州市
    # city_codes = ['320505','320506','320507','320508','320509','320581','320582','320583','320585']

    for city_code in city_codes:
        download_each_city(city_code)


def main():
    # 解析配置文件
    CONF.parse_from_file('config.yml')
    print(CONF.key)

    city_code_item = CityCode()
    city_codes = city_code_item.fetch_city_code_for_spider()
    for city_code in city_codes:
        download_each_city(city_code)


def down_load_data_by_polygon():
    # 解析配置文件
    CONF.parse_from_file('config/config.yml')

    city_codes = [116.34459731000003, 40.10685308500017, 116.63942421000012, 39.80852284500011]
    i = 0
    AmapSpider.write_json_before()
    while city_codes[0] + 0.2 * i < city_codes[2]:
        temp_code = [city_codes[0] + 0.2 * i,0,city_codes[0] + 0.2 * i + 0.2,0]
        j = 0
        while city_codes[3] + 0.2 *j < city_codes[1]:
            temp_code[1] = city_codes[3] + 0.2 + 0.2 *j
            temp_code[3] = city_codes[3] + 0.2 * j
            hospital_count = 0
            for spider_type in CONF.types:
                if hospital_count != 0:
                    connect_char = ','
                else:
                    connect_char = ''
                amap_spider = AmapSpider(CONF.key, spider_type, temp_code, connect_char, 'polygon')
                hospital_count = amap_spider.get_poi_data()
            print(temp_code)
            j += 1
        i += 1
    AmapSpider.write_json_after()
    AmapSpider.write_data_to_excel('temp_data3/{0}'.format('test'))


if __name__ == '__main__':
    # down_load_data()
    down_load_data_by_polygon()
