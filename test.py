import pandas as pd

if __name__ == '__main__':
    hospital = pd.read_csv('China_hospital.csv')
    # print(hospital.columns.values)
    # print(hospital['医院大类'].unique())
    # print(hospital['医院次类'].unique())
    # print(hospital['医院小类'].unique())
    hospital = hospital[hospital['城市名称'] == '东莞市']
    print(hospital)