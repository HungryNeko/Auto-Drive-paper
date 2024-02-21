'''
Descripttion: 用于读取GIS上的道路经纬度信息(pekingroad.geojson文件), 并通过isIn5.py, 提取五环内的道路
version: 
Author: 胡睿杰, 何时
Date: 2023-10-15 09:41:31
LastEditors: Andy
LastEditTime: 2024-01-23 12:56:04
'''
import json
import isIn5
'''
Descripttion: 读取JSON文件, 写入到roadinf.txt文件
return value {*}
'''
def readjson():
    # 读取JSON文件
    with open('pekingrode.geojson', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # 初始化一个字典用于存储处理后的数据
    processed_data = []

    # 遍历features
    for feature in data['features']:
        osm_id = feature['properties']['osm_id']
        name = feature['properties']['name']
        coordinates = feature['geometry']['coordinates']

        # 计算坐标的平均经度和纬度
        avg_longitude = sum(coord[0] for coord in coordinates[0]) / len(coordinates[0])
        avg_latitude = sum(coord[1] for coord in coordinates[0]) / len(coordinates[0])

        # 创建包含所需信息的字典
        road_info = {
            "osm_id": osm_id,
            "name": name,
            "coordinates": coordinates,
            "avglon": avg_longitude,  # 存为"avglon"
            "avglat": avg_latitude  # 存为"avglat"
        }

        processed_data.append(road_info)

    # 写入到roadinf.txt文件
    with open('roadinf.txt', 'w', encoding='utf-8', buffering = 8192) as txt_file:
        for road_info in processed_data:
            txt_file.write(json.dumps(road_info, ensure_ascii=False) + '\n')

'''
Descripttion: 读取JSON文件, 通过isIn5.py, 提取五环内的道路, 写入到roadinfof5.txt文件 
return value {*}
'''
def deleteOut5():
    # 读取JSON文件
    with open('roadinf.txt', 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()

    # 初始化一个列表用于存储满足条件的数据
    filtered_data = []

    # 遍历每一行数据
    for line in lines:
        road_info = json.loads(line)
        avg_longitude = road_info['avglon']
        avg_latitude = road_info['avglat']

        # 调用carIsIn5函数检查坐标是否满足条件
        if isIn5.carIsIn5(avg_longitude, avg_latitude):
            filtered_data.append(road_info)

    # 将满足条件的数据写回roadinfof5.txt文件
    with open('roadinfof5.txt', 'w', encoding='utf-8', buffering = 8192) as txt_file:
        for road_info in filtered_data:
            txt_file.write(json.dumps(road_info, ensure_ascii=False) + '\n')

readjson()
deleteOut5()