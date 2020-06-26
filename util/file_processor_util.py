# coding=utf-8
# auther=Xiao Yijia

import csv
import os

import xlrd

from config import CONF


class FileProcessorUtil(object):

    @classmethod
    def combine_file_list(cls, file_list, outfile_name):
        method = 'w'
        head = CONF.hkeys
        for file_name in file_list:
            print(file_name)
            infile_suffix = os.path.splitext(file_name)[1]
            if infile_suffix == '.xls':
                datas = FileProcessorUtil.fetch_excel_data(file_name)
            else:
                datas = []
            outfile_suffix = os.path.splitext(outfile_name)[1]
            if outfile_suffix == '.csv':
                FileProcessorUtil.write_to_csv_file(outfile_name, datas, method, head)
                method = 'a'
                head = None
            elif outfile_suffix == '.xls':
                pass

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


if __name__ == '__main__':
    CONF.parse_from_file('../config.yml')
    FileProcessorUtil.combine_path_file(r'../data', '../China_hospital.csv')
    # FileProcessorUtil.combine_file_list(['../data/110101.xls', '../data/110102.xls'], '../test.csv')
