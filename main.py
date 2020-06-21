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
        AmapSpider.write_json_before()
        amap_spider = AmapSpider(CONF.key, CONF.types[0], city_code, '')
        hospital_count = amap_spider.get_poi_data()
        city_code_item.write_finish_city_code(city_code, CONF.types[0], hospital_count)
        for spider_type in CONF.types[1:]:
            amap_spider = AmapSpider(CONF.key, spider_type, city_code, ',')
            hospital_count = amap_spider.get_poi_data()
            city_code_item.write_finish_city_code(city_code, spider_type, hospital_count)
        AmapSpider.write_json_after()
        AmapSpider.write_data_to_excel('data/{0}'.format(city_code))
        city_code_item.save()
    pass


if __name__ == '__main__':
    main()
