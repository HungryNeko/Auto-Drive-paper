'''
Descripttion: 通过folder_path变量，读取所有该文件夹下的txt文件，通过两个连贯的车辆数据点，计算出当前车辆的速度，加速度与角速度作为一个新的车辆数据 
version: 
Author: 胡睿杰
Date: 2023-10-15 09:41:30
LastEditors: Andy
LastEditTime: 2024-01-23 13:10:28
'''
import os
from datetime import datetime
# 引入cacaltion.py中的函数
from calculation import calculate, car_dict
import concurrent.futures
'''
Descripttion: 读取所有file_name文件夹下的txt文件，并将车辆信息保存到car_dict的字典中 
return value {*}
'''
# car_dict -> 用来存储车辆信息(按照车辆分类)
def readin(file_name):
    file_path = os.path.join(root, file_name)
    with open(file_path, 'r') as file:
        for line in file:
            elements = line.strip().split(",")
            car_dict.setdefault(elements[0], []).append({
                'time': datetime.strptime(elements[1], "%Y-%m-%d %H:%M:%S"),
                'longitude': float(elements[2]),
                'latitude': float(elements[3])
            })

# 计算所有车辆的信息
def cal_information(i):
    calculate(str(i))

'''
Descripttion: 覆盖原来的log.txt文件与error_data.txt文件，计算出车辆当前的数据，并通过速度判断该数据点是否有误，若有误则放入到error_data.txt文件中，若无误则放入到log.txt中
return value {*}
'''
if __name__ == "__main__":
    folder_path = '../01'
    with open('log.txt', 'w') as log_file: pass
    with open('error_data.txt', 'w') as error_file: pass
    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(folder_path):
            executor.map(readin, files)

    # Create another ThreadPoolExecutor for cal_information
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(cal_information, range(1, 10357))
