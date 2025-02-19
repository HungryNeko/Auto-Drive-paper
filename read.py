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


def readtxt(root,full=False,wgs84=False,limit=False):

    with open(root, 'r') as log_file:
        lines = log_file.readlines()
    count=0
    for line in tqdm(lines, desc=f"Processing {root}"):
        count+=1
        try:
            parts = line.strip().split(',')
            lon, lat = float(parts[-2]), float(parts[-1])
            #print(lon,lat)
            gcj=[]
            if wgs84==True:
                gcj=wgs84Togcj02.wgs84togcj02(lon,lat)
                #print(gcj)
                lon=float(gcj[0])
                lat=float(gcj[1])

            if full:
                dict_data.setdefault(parts[0], []).append({
                    'id':parts[0],
                    'time': datetime.datetime.strptime(parts[1], "%Y-%m-%d %H:%M:%S"),
                    'lon': lon,
                    'lat': lat,
                    'speed': float(parts[2]),
                    'acceleration': float(parts[3]),
                    'angle': float(parts[4]),
                    # 'nearest_road_id': '',
                    # 'nearest_road_name': ''
                })
                #print(lon, lat)
            else:
                dict_data.setdefault(parts[0], []).append({
                    'id': parts[0],
                    'time': datetime.datetime.strptime(parts[1], "%Y-%m-%d %H:%M:%S"),
                    'lon': lon,
                    'lat': lat,
                    #'speed': float(parts[2]),
                    #'acceleration': float(parts[3]),
                    #'angle': float(parts[4]),
                    # 'nearest_road_id': '',
                    # 'nearest_road_name': ''
                })
                #print(lon, lat)

        except Exception as e:
            #print(f"Error in line : {line}")
            #print(e)
            continue  # Skip to the next iteration
        if count==limit:
            break


def readroad():
    with open('roadinfof5.txt', 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()

    for line in lines:
        road_info = json.loads(line)
        osm_id = road_info['osm_id']
        road_info_dict[osm_id] = road_info