# coding=utf-8
# auther=Xiao Yijia
import csv
import os

import pandas as pd
import xlrd
import xlwt

from config.city_code import city_dict
from config.config import CONF


class FileProcessorUtil(object):

    @classmethod
    def add_field(cls, datas, columns, field_name, field_value):
        pd_datas = pd.DataFrame(datas, columns=columns)
        pd_datas[field_name] = field_value
        columns = columns + [field_name]
        return pd_datas[columns].values, columns

    @classmethod
    def combine_file_list(cls, file_list, outfile_name):
        method = 'w'
        head = CONF.hkeys + ['City_Code']
        for file_name in file_list:
            columns = CONF.hkeys
            _, infile_name, infile_suffix = FileProcessorUtil.parse_path(file_name)
            city_code = FileProcessorUtil.get_city_code(infile_name)
            print(infile_name, city_code)
            if infile_name == '442101':
                continue
            if infile_suffix == '.xls':
                datas = FileProcessorUtil.fetch_excel_data(file_name)
                datas, columns = FileProcessorUtil.add_field(datas, columns, 'City_code',
                                                             FileProcessorUtil.get_city_code(infile_name))
                datas, columns = FileProcessorUtil.data_deduplication(datas, columns, ['经度', '纬度', '医院小类'])
            else:
                datas = []
            _, _, outfile_suffix = FileProcessorUtil.parse_path(outfile_name)
            if outfile_suffix == '.csv':
                FileProcessorUtil.write_to_csv_file(outfile_name, datas, method, head)
                method = 'a'
                head = None
            elif outfile_suffix == '.xls':
                pass

    @classmethod
    def get_city_code(cls, original_code):
        if original_code.startswith('3712'):
            code = 370100
        elif original_code.startswith('5424'):
            code = 540600
        else:
            code = int(original_code)
        if str(code) in city_dict.keys():
            return code
        code = int(int(original_code) / 100) * 100
        if str(code) in city_dict.keys():
            return code
        code = int(int(original_code) / 10000) * 10000
        if str(code) in city_dict.keys():
            return code
        else:
            print('####################################################Not Found in city_dict    ' + original_code)
            return original_code

    @classmethod
    def combine_path_file(cls, input_path, out_file_name, suffix=''):
        file_list = []
        for file_name in os.listdir(input_path):
            if suffix == '' or os.path.splitext(file_name)[1] == suffix:
                file_list.append(os.path.join(input_path, file_name))
        FileProcessorUtil.combine_file_list(file_list, out_file_name)

    @classmethod
    def fetch_excel_data(cls, file_name, head=False):
        datas = []
        data_sheet = xlrd.open_workbook(file_name).sheet_by_index(0)
        if head:
            datas.append(data_sheet.row_values(0))
        for i in range(1, data_sheet.nrows):
            datas.append(data_sheet.row_values(i))
        return datas

    @classmethod
    def write_to_csv_file(cls, file_name, datas, method='a', head=None, charset='utf-8'):
        with open(file_name, method, newline='', encoding=charset) as file:
            file_writer = csv.writer(file)
            if head is not None:
                file_writer.writerow(head)
            for data in datas:
                file_writer.writerow(data)

    @classmethod
    def data_deduplication(cls, datas, columns, by_index):
        pd_datas = pd.DataFrame(datas, columns=columns)
        data_deduplication_data = pd_datas.groupby(by=by_index).first()
        data_deduplication_data.reset_index(inplace=True)
        return data_deduplication_data[columns].values, columns

    @classmethod
    def parse_path(cls, file_path):
        shp_path = os.path.dirname(file_path)
        shp_name_suffix = os.path.split(file_path)[-1]
        shp_name = shp_name_suffix.split('.')[0]
        shp_suffix = shp_name_suffix[len(shp_name):]
        return shp_path, shp_name, shp_suffix

    @classmethod
    def clean_data(cls, filename, order_list):
        datas = FileProcessorUtil.fetch_excel_data(filename, False)
        for data in datas:
            if data[5].find('|') > 0:
                types = data[5].split('|')
                types[0] = data[3] + ';' + data[4] + ';' + types[0]
                detail_type = [simple_type.split(';')[1] for simple_type in types]
                mark = False
                for order in order_list:
                    if order in detail_type:
                        mark = True
                        for i in range(len(detail_type)):
                            if detail_type[i] == order:
                                data[3], data[4], data[5] = types[i].split(';')
                                break
                        break
                if not mark:
                    data[3], data[4], data[5] = types[0].split(';')

        # for i in range(datas)
        pd_datas = pd.DataFrame(datas, columns=CONF.hkeys)
        pd_datas = pd_datas[pd_datas['医院大类'] == '医疗保健服务']
        # 实例化一个Workbook()对象(即excel文件)
        wbk = xlwt.Workbook()
        # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
        sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

        # 创建表头
        # for循环访问并获取数组下标enumerate函数
        for index, hkey in enumerate(CONF.hkeys):
            sheet.write(0, index, hkey)

        datas = pd_datas.values
        row, col = datas.shape
        for i in range(row):
            values = datas[i]
            n = i + 1
            for j in range(col):
                sheet.write(n, j, values[j])
        wbk.save(filename)
        # for data in datas:
        #     print(data)

    @classmethod
    def data_deduplication_hospital(cls, filename, input_path, out_path):
        if not os.path.exists(out_path):
            os.mkdir(out_path)
        datas = FileProcessorUtil.fetch_excel_data(input_path + '\\' + filename, False)
        for data in datas:
            index = data[2].find('医院')
            if index >= 0:
                data[2] = data[2][:index + 2]
        datas, columns = FileProcessorUtil.data_deduplication(datas, CONF.hkeys, ['医院名称'])
        # 实例化一个Workbook()对象(即excel文件)
        wbk = xlwt.Workbook()
        # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
        sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

        # 创建表头
        # for循环访问并获取数组下标enumerate函数
        for index, hkey in enumerate(columns):
            sheet.write(0, index, hkey)

        row, col = datas.shape
        for i in range(row):
            values = datas[i]
            n = i + 1
            for j in range(col):
                sheet.write(n, j, values[j])
        wbk.save(out_path + '\\' + filename)
        pass

    @classmethod
    def dirty_data_output(cls, filename, input_path, out_path):
        if not os.path.exists(out_path):
            os.mkdir(out_path)
        datas = FileProcessorUtil.fetch_excel_data(input_path + '\\' + filename, False)
        for data in datas:
            index = data[2].find('医院')
            if index >= 0:
                data[2] = data[2][:index + 2]
        ori_data = pd.DataFrame(datas, columns=CONF.hkeys)
        pd_datas = ori_data.groupby(by=['医院名称'])['id'].count().to_frame()
        repeat_hospital = pd_datas[pd_datas['id'] > 1].index.tolist()

        # 实例化一个Workbook()对象(即excel文件)
        wbk = xlwt.Workbook()
        # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
        sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

        # 创建表头
        # for循环访问并获取数组下标enumerate函数
        for index, hkey in enumerate(CONF.hkeys):
            sheet.write(0, index, hkey)

        n = 1
        for data in datas:
            if data[2] in repeat_hospital:
                for j in range(len(data)):
                    sheet.write(n, j, data[j])
                n += 1
        wbk.save(out_path + '\\' + filename)
        pass



def patch_data_clean():
    CONF.parse_from_file('../config/config.yml')
    order_list = ['综合医院', '专科医院', '急救中心', '医疗保健服务场所', '诊所', '疾病预防机构', '医药保健销售店', '动物医疗场所']
    for filename in os.listdir('../data'):
        if filename.endswith('.xls'):
            print('../data/' + filename)
            FileProcessorUtil.clean_data('../data/' + filename, order_list)

def patch_data_deduplication():
    CONF.parse_from_file('../config/config.yml')
    for filename in os.listdir('../data'):
        if filename.endswith('.xls'):
            print(filename)
            FileProcessorUtil.data_deduplication_hospital(filename, '../data', '../data_finish')
            FileProcessorUtil.dirty_data_output(filename, '../data', '../data_dirty')


def combine_data():
    CONF.parse_from_file('../config/config.yml')
    # FileProcessorUtil.combine_path_file(r'../data_finish', '../China_hospital_finish.csv')
    FileProcessorUtil.combine_path_file(r'../data_finish', '../China_hospital_20200719.csv')


def split_data(filename, output_path):
    CONF.parse_from_file('../config/config.yml')
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    pd_datas = pd.read_csv(filename, encoding='utf-8')
    print(pd_datas)
    city_codes = [k for k,v in city_dict.items()]
    for city_code in city_codes:
        if city_code == '440800':
            continue
        if city_code == '510700':
            continue

        print(city_code)
        tmp_data = pd_datas[pd_datas['City_Code'] == int(city_code)]
        tmp_data.to_csv(output_path + '\\' + city_code + '.csv', index=None, encoding='gbk')
    print(city_codes)
    pass


def test(fn):
    with open(fn, 'rb+') as fp:
        content = fp.read()
        content = content.decode('utf-8').encode('gbk')
        fp.seek(0)
        fp.write(content)
    pass


def file_count(city_codes):
    count = 0
    for city_code in city_codes:
        datas = FileProcessorUtil.fetch_excel_data('F:/git/amap_pois_fetch/temp_data2/{0}.xls'.format(city_code))
        count += len(datas)
    print(count)


def file_count_path(file_path):
    count = 0
    for file in os.listdir(file_path):
        if file.endswith('.xls'):
            datas = FileProcessorUtil.fetch_excel_data(os.path.join(file_path, file))
            count += len(datas)
    print(count)

if __name__ == '__main__':
    # combine_data()
    # patch_data_clean()
    # patch_data_deduplication()
    # split_data('../China_hospital_20200719.csv', '../city_data2')
    # for file in os.listdir('../city_data'):
    #     if file.endswith('.csv'):
    #         print(file)
    #         test('../city_data/' + file)

    # 南京市
    city_codes = ['320102', '320104', '320105', '320106', '320111', '320113', '320114', '320115', '320116', '320117', '320118']
    # 合肥市
    # city_codes = ['340102','340103','340104','340111','340121','340122','340123','340124','340181']
    # 徐州市
    # city_codes = ['320302','320303','320305','320311','320312','320321','320322','320324','320381','320382']
    # 苏州市
    # city_codes = ['320505','320506','320507','320508','320509','320581','320582','320583','320585']
    file_count(city_codes)
    # file_count_path(r'F:\git\amap_pois_fetch\temp_data')