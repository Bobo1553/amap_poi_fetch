# coding=utf-8
# author=Yijia Xiao
from config import CONF
from util.amap import AmapSpider
from util.citycode import CityCode


def main():
    # 解析配置文件
    CONF.parse_from_file('config.yml')
    print(CONF.key)

    city_code_item = CityCode()
    city_codes = city_code_item.fetch_city_code_for_spider()
    for city_code in city_codes:
        connect_char = ''
        AmapSpider.write_json_before()
        hospital_count = 0
        for spider_type in CONF.types:
            if hospital_count != 0:
                connect_char = ','
            amap_spider = AmapSpider(CONF.key, spider_type, city_code, connect_char)
            hospital_count = amap_spider.get_poi_data()
            city_code_item.write_finish_city_code(city_code, spider_type, hospital_count)
        AmapSpider.write_json_after()
        AmapSpider.write_data_to_excel('data/{0}'.format(city_code))
        city_code_item.save()
    pass


if __name__ == '__main__':
    main()
