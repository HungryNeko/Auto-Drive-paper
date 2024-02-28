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
dict_data = {}
road_info_dict = {}

def wgs84_to_gcj02(lon, lat):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:4490", always_xy=True)
    gcj_lon, gcj_lat = transformer.transform(lon, lat)
    return gcj_lon, gcj_lat

def readtxt(root):
    with open(root, 'r') as log_file:
        lines = log_file.readlines()

    for line in lines:
        try:
            parts = line.strip().split(',')
            lon, lat = float(parts[2]), float(parts[3])
            #gcj_lon, gcj_lat = wgs84_to_gcj02(lon, lat)
            #gcj_lon, gcj_lat =lon, lat
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

        except IndexError:
            print(f"Error in line : {line}")
            continue  # Skip to the next iteration


def readroad():
    with open('roadinfof5.txt', 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()

    for line in lines:
        road_info = json.loads(line)
        osm_id = road_info['osm_id']
        road_info_dict[osm_id] = road_info