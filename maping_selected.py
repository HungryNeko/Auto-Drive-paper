"""
直接读取已筛选数据并打印统计信息
"""

import pyproj
import numpy as np
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
from multiprocessing import Pool
from shapely.ops import transform
from read import readtxt, dict_data  # Assuming readtxt and dict_data functions are defined in the 'read' module
from shapely.geometry import Point, LineString, Polygon
import save_load

def create_road_polygon(trajectory):
    line = LineString(trajectory)
    transformer = pyproj.Transformer.from_crs('epsg:4490', 'epsg:32650', always_xy=True)
    line_transformed = transform(transformer.transform, line)
    left_line = line_transformed.parallel_offset(11.25, 'left')
    right_line = line_transformed.parallel_offset(11.25, 'right')
    transformer = pyproj.Transformer.from_crs('epsg:32650', 'epsg:4490', always_xy=True)
    left_line = transform(transformer.transform, left_line)
    right_line = transform(transformer.transform, right_line)
    road_polygon = Polygon(np.concatenate([left_line.xy, np.fliplr(right_line.xy)], axis=1).T)
    return road_polygon

def check_point_on_road():
    #print(datalist)
    result = []
    for point in datalist:
        result.append((point['speed'], point['acceleration'], point['angle']))
    return [result]

def plot_trajectories(trajectories, datalist):
    speed_data = []
    acceleration_data = []
    angle_data = []

    with Pool() as p:
        print("!")
        for result in check_point_on_road():
            if result is not None:
                for speed, acceleration, angle in result:
                    speed_data.append(speed)
                    acceleration_data.append(acceleration)
                    angle_data.append(angle)

    fig, axs = plt.subplots(3, 1, figsize=(10, 24))  # 创建一个3行1列的图形数组

    sns.histplot(speed_data, bins=30, kde=True, ax=axs[0])  # 在第一个子图上绘制速度数据
    sns.histplot(acceleration_data, bins=30, kde=True, ax=axs[1])  # 在第二个子图上绘制加速度数据
    sns.histplot(angle_data, bins=30, kde=True, ax=axs[2])  # 在第三个子图上绘制角度数据
    axs[0].set_title('speed distribution')
    axs[1].set_title('acceleration distribution')
    axs[2].set_title('angle distribution')
    plt.show()

anglelimit = [90.0, 270.0]  # 目标>angle[0] <angle[1]

if __name__ == "__main__":
    datalist = save_load.loaddata("data东四环中路_segmented_in_2min.txt")
    #print(datalist)
    file = './路网数据/东四环中路.txt'
    with open(file, 'r') as f:
        data = eval(f.read())

    road_polygons = [create_road_polygon(trajectory) for trajectory in data]

    plot_trajectories(road_polygons, datalist)
