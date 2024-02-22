import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
from pyproj import CRS, Transformer
from read import readtxt, dict_data  # Assuming readtxt and dict_data functions are defined in the 'read' module
from multiprocessing import Pool
from tqdm import tqdm
from functools import partial
from shapely.ops import transform
from functools import partial
import pyproj
import matplotlib.cm as cm
import matplotlib.patches as mpatches

def plot_road(trajectory, width=22.5, style='-', color='black'):
    line = LineString(trajectory)
    # 创建一个转换器，将WGS84坐标转换为UTM坐标
    transformer = pyproj.Transformer.from_crs('epsg:4326', 'epsg:32650', always_xy=True)
    line_transformed = transform(transformer.transform, line)
    # 创建道路的两侧线
    left_line = line_transformed.parallel_offset(width / 2, 'left')
    right_line = line_transformed.parallel_offset(width / 2, 'right')
    # 将UTM坐标转换回WGS84坐标
    transformer = pyproj.Transformer.from_crs('epsg:32650', 'epsg:4326', always_xy=True)
    left_line = transform(transformer.transform, left_line)
    right_line = transform(transformer.transform, right_line)
    # 绘制道路的两侧线
    ax.plot(*left_line.xy, style, color=color)
    ax.plot(*right_line.xy, style, color=color)
    # ax.plot(*line.xy, '--', color=color)  # 使用虚线绘制中心线

def check_point_on_road(args):
    point_data, trajectories, i, j = args
    point = Point(point_data['lon'], point_data['lat'])
    for trajectory in trajectories:
        road = LineString(trajectory)
        if road.buffer(0.0001).contains(point):  # Adjust the buffer size as needed
            return (point_data['lon'], point_data['lat'], str(point_data['time']), i, j)
    return None

def plot_trajectories(trajectories, dict_data):
    colors = cm.rainbow(np.linspace(0, 1, len(dict_data)))
    patches = []
    for i, (car_id, car_data) in enumerate(dict_data.items()):
        # 先筛选出在道路内的数据点
        args = [(point_data, trajectories, i, j) for j, point_data in enumerate(car_data)]
        with Pool() as p:
            results = [result for result in tqdm(p.imap(check_point_on_road, args), total=len(args)) if result is not None]
        # 对在道路内的数据点按照时间顺序进行排序
        results.sort(key=lambda x: x[2])  # Use the time as the key for sorting
        for k, result in enumerate(results):
            lon, lat, time, i, j = result
            ax.scatter(lon, lat, color=colors[i])
            ax.text(lon, lat, str(k))  # Use the index as the label, starting from 0 for each car
        patches.append(mpatches.Patch(color=colors[i], label=car_id))

    plt.legend(handles=patches)


if __name__ == "__main__":
    file = './路网数据/东二环.txt'
    with open(file, 'r') as f:
        data = eval(f.read())

    readtxt('log.txt')

    fig, ax = plt.subplots(figsize=(10, 8))

    # 绘制道路
    for trajectory in data:
        plot_road(trajectory)

    plot_trajectories(data, dict_data)

    plt.axis('equal')
    plt.show()
