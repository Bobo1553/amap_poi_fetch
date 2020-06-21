# coding=utf-8
# @auther=Yijia Xiao

import configparser


class CONF:
    key = None
    types = None
    page_size = None
    json_name = None
    hkeys = None
    bkeys = None

    @staticmethod
    def parse_from_file(filename):
        conf = configparser.ConfigParser()
        conf.read(filename, encoding='utf-8')
        CONF.key = conf['spider']['key']
        CONF.types = [spider_type for spider_type in conf['spider']['types'].split(';')]
        CONF.page_size = int(conf['spider']['page_size'])

        CONF.json_name = conf['file']['json_name']
        CONF.hkeys = [hkey for hkey in conf['file']['hkeys'].split(';')]
        CONF.bkeys = [bkey for bkey in conf['file']['bkeys'].split(';')]
        pass


if __name__ == '__main__':
    CONF.parse_from_file('config.yml')
    print(CONF.key)
    print(CONF.types)
    print(CONF.page_size)
    print(CONF.json_name)
    print(CONF.hkeys)
    print(CONF.bkeys)
