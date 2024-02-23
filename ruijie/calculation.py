'''
Descripttion: 
    计算两个经纬度之间的距离，单位米
    计算两个经纬度之间的方位角
    通过两个车辆静态数据，计算该车辆在两个静态数据间的实时数据，通过速度来判断该数据是否有误，来区分放入到log.txt(数据无误)，还是error_data.txt(数据有误)中        
version: 
Author: 胡睿杰, 何时
Date: 2023-10-18 11:50:58
LastEditors: Andy
LastEditTime: 2024-02-23 11:17:03
'''

from isIn5 import carIsIn5
from math import radians, sin, cos, sqrt, atan2, degrees

car_dict = {}
earth_radius_km = 6371.393

# def decimal5(num):
#     int(round(num * 100000) / 100000)
'''
Descripttion: 计算两个经纬度之间的距离，单位米
return value {两个经纬度之间的距离，单位米}
param {*} x1 前一个数据的经度
param {*} y1 前一个数据的纬度
param {*} x2 后一个数据的经度
param {*} y2 后一个数据的纬度
'''
def distanceCal(x1, y1, x2, y2):
    x1 = radians(x1); y1 = radians(y1); x2 = radians(x2); y2 = radians(y2)
    a = sin((y2 - y1) / 2) ** 2 + cos(y1) * cos(y2) * sin((x2 - x1)/ 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return earth_radius_km * c * 1000

'''
Descripttion: 计算两个经纬度之间的方位角
return value {两个经纬度之间的方位角}
param {*} x1 前一个数据的经度
param {*} y1 前一个数据的纬度
param {*} x2 后一个数据的经度
param {*} y2 后一个数据的纬度
'''
def bearingCal(x1, y1, x2, y2):
    x1 = radians(x1); y1 = radians(y1); x2 = radians(x2); y2 = radians(y2)
    a = cos(y1) * sin(y2) - sin(y1) * cos(y2) * cos(x2 - x1)
    b = sin(x2 - x1) * cos(y2)
    bearing = atan2(b, a)
    return (degrees(bearing) + 360) % 360
'''
Descripttion: 通过两个车辆静态数据，计算该车辆在两个静态数据间的实时数据，通过速度来判断该数据是否有误，来区分放入到log.txt(数据无误)，还是error_data.txt(数据有误)中        
return value {*}
param {*} id 该车辆的id
'''
def calculate(id):
    car_result = {}
    sorted_data = []
    if id in car_dict:
        data_for_id = car_dict[id]
        if not data_for_id: return
        sorted_data = sorted(data_for_id, key=lambda x: x['time'])

    x1 = x2 = sorted_data[0]['longitude']; y1 = y2 = sorted_data[0]['latitude']; t1 = t2 = sorted_data[0]['time']

    for data_entry in sorted_data[1:]:
        x1 = x2; y1 = y2; t1 = t2
        x2 = data_entry['longitude']; y2 = data_entry['latitude']; t2 = data_entry['time']
        dt = t2 - t1
        distance = distanceCal(x1, y1, x2, y2)
        if dt.total_seconds() == 0 or distance == 0: continue
        speed = distance / dt.total_seconds()        
        acceleration = speed / dt.total_seconds()
        angle = bearingCal(x1, y1, x2, y2)
        if not carIsIn5(x2, y2): continue
        else:
            car_result.setdefault(id, []).append({
                'time': t2,
                'speed': round(speed, 5),
                'acceleration': round(acceleration, 5),
                'angle': round(angle, 5),
                'lon': round(data_entry['longitude'], 5),
                'lat': round(data_entry['latitude'], 5)
            })

    with open('log.txt', 'a', buffering=8192) as log_file:
        for key, values in car_result.items():
            for entry in values:
                if all(entry.get(field) is not None for field in ['time', 'speed', 'acceleration', 'angle', 'lon', 'lat']):
                    if entry['speed'] >= 34 or entry['speed'] <= 0 or entry['acceleration'] < -3 or entry['acceleration'] > 3:
                        with open('error_data.txt', 'a', buffering=8192) as error_file:
                            error_file.write(f"{key},{entry['time']},{entry['speed']},{entry['acceleration']},{entry['angle']},{entry['lon']},{entry['lat']}\n")
                    else:
                        log_file.write(f"{key},{entry['time']},{entry['speed']},{entry['acceleration']},{entry['angle']},{entry['lon']},{entry['lat']}\n")
