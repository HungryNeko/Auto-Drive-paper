'''
Descripttion: 
version: 
Author: 胡睿杰
Date: 2023-10-22 16:11:25
LastEditors: Andy
LastEditTime: 2024-01-27 12:22:43
'''
import json
import datetime

dict_data = {}
road_info_dict = {}

def readtxt(root):
    with open(root, 'r') as log_file:
        lines = log_file.readlines()

    for line in lines:
        try:
            parts = line.strip().split(',')
            
            dict_data.setdefault(parts[0], []).append({
                'time': datetime.datetime.strptime(parts[1], "%Y-%m-%d %H:%M:%S"),
                'lon': float(parts[5]),
                'lat': float(parts[6]),
                'speed': float(parts[2]),
                'acceleration': float(parts[3]),
                'angle': float(parts[4]),
                # 'nearest_road_id': '',
                # 'nearest_road_name': ''
            })

        except IndexError:
            #print(f"Error in line : {line}")
            continue  # Skip to the next iteration
        except ValueError:
            continue
    print('read finished')

def readroad():
    with open('roadinfof5.txt', 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()

    for line in lines:
        road_info = json.loads(line)
        osm_id = road_info['osm_id']
        road_info_dict[osm_id] = road_info