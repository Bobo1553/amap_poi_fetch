# Amap_poi_fetch
基于Python3实现高德地图POI检索数据获取，并写入exce文件。

1. 根据自己的需求修改config.yml
2. 修改AMap_API_Table/高德地图API 城市编码对照表.xls
   * sheet2设置你需要爬取的数据
   * sheet3为你已经爬取完后的数据，如果重新或者第一次开始爬取的话，清空除去表头外的sheet3
3. 运行main.py，按照城市的编码保存数据，生成的数据保存在data文件夹下

#### PS

现有data下是已经爬取的一些城区的医疗点数据