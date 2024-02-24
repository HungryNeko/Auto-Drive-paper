"""
在show.py的基础上，手动设置一条垂直于路面的垂线，显示为红色，用不同颜色表示不同方向行驶的车辆
"""
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

# 定义绘制道路函数
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

# 定义检查车辆位置函数
def check_point_on_road(args):
    point_data, trajectories, i = args
    point = Point(point_data['lon'], point_data['lat'])
    for trajectory in trajectories:
        road = LineString(trajectory)
        if road.buffer(0.0001).contains(point):  # Adjust the buffer size as needed
            return (point_data['lon'], point_data['lat'], str(point_data['time']), i)
    return None

# 定义绘制轨迹函数
def plot_trajectories(trajectories, point1, point2):
    # 绘制道路
    for trajectory in data:
        plot_road(trajectory)

    # 绘制垂线
    plt.plot([point1[0], point2[0]], [point1[1], point2[1]], color='red')

    # 绘制车辆位置
    colors = cm.rainbow(np.linspace(0, 1, len(dict_data)))
    args = []
    patches = []  # 图例
    for i, (car_id, car_data) in enumerate(dict_data.items()):
        for point_data in car_data:
            args.append((point_data, trajectories, i))
        patches.append(mpatches.Patch(color=colors[i], label=car_id))

    with Pool() as p:
        for result in tqdm(p.imap(check_point_on_road, args), total=len(args)):
            if result is not None:
                lon, lat, time, i = result
                ax.scatter(lon, lat, color=colors[i])

    plt.legend(handles=patches)

if __name__ == "__main__":
    file = './路网数据/北三环.txt'
    with open(file, 'r') as f:
        data = eval(f.read())

    # 设置垂线的两个端点坐标
    point1 = [116.43249, 39.95362]
    point2 = [116.44103, 39.97796]

    # 读取车辆数据
    357readtxt('log.txt')

    fig, ax = plt.subplots(figsize=(10, 8))

    # 调用绘制轨迹函数
    plot_trajectories(data, point1, point2)

    plt.axis('equal')
    plt.show()
