'''
Descripttion: 
version: 
Author: 胡睿杰
Date: 2023-10-22 16:11:25
LastEditors: Andy
LastEditTime: 2024-02-01 12:13:44
'''
import json
import datetime
from pyproj import Transformer
from tqdm import tqdm

import wgs84Togcj02

dict_data = {}
road_info_dict = {}


def readtxt(root,wgs84=False):
    with open(root, 'r') as log_file:
        lines = log_file.readlines()

    for line in tqdm(lines, desc=f"Processing {root}"):
        try:
            parts = line.strip().split(',')
            lon, lat = float(parts[2]), float(parts[3])
            if wgs84==True:
                gcj=wgs84Togcj02.wgs84togcj02(lon,lat)
                lon=gcj[0],lat=gcj,[1]
            dict_data.setdefault(parts[0], []).append({
                'time': datetime.datetime.strptime(parts[1], "%Y-%m-%d %H:%M:%S"),
                'lon': lon,
                'lat': lat,
                #'speed': float(parts[2]),
                #'acceleration': float(parts[3]),
                #'angle': float(parts[4]),
                # 'nearest_road_id': '',
                # 'nearest_road_name': ''
            })

            # 如果数据存在，尝试转换为浮点数，否则设置为 None
            try:
                speed = float(parts[2])
            except (IndexError, ValueError):
                speed = None

            try:
                acceleration = float(parts[3])
            except (IndexError, ValueError):
                acceleration = None

            try:
                angle = float(parts[4])
            except (IndexError, ValueError):
                angle = None

            # 将转换后的数据添加到字典中
            dict_data[parts[0]][-1]['speed'] = speed
            dict_data[parts[0]][-1]['acceleration'] = acceleration
            dict_data[parts[0]][-1]['angle'] = angle

        except Exception:
            #print(f"Error in line : {line}")
            continue  # Skip to the next iteration


def readroad():
    with open('roadinfof5.txt', 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()

    for line in lines:
        road_info = json.loads(line)
        osm_id = road_info['osm_id']
        road_info_dict[osm_id] = road_info