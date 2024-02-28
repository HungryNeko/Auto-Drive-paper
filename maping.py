import pyproj
import numpy as np
from tqdm import tqdm
import matplotlib.cm as cm
from functools import partial
import matplotlib.pyplot as plt
from multiprocessing import Pool
from shapely.ops import transform
from read import readtxt, dict_data  # Assuming readtxt and dict_data functions are defined in the 'read' module
import matplotlib.patches as mpatches
from shapely.geometry import Point, LineString, Polygon

def plot_road(trajectory, width=11.25, style='-', color='black'):
    line = LineString(trajectory)
    transformer = pyproj.Transformer.from_crs('epsg:4490', 'epsg:32650', always_xy=True)
    line_transformed = transform(transformer.transform, line)
    left_line = line_transformed.parallel_offset(width, 'left')
    right_line = line_transformed.parallel_offset(width, 'right')
    transformer = pyproj.Transformer.from_crs('epsg:32650', 'epsg:4490', always_xy=True)
    left_line = transform(transformer.transform, left_line)
    right_line = transform(transformer.transform, right_line)
    ax.plot(*left_line.xy, style, color=color)
    ax.plot(*right_line.xy, style, color=color)
    # ax.plot(*line.xy, '--', color=color)  # 使用虚线绘制中心线

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

def check_point_on_road(args):
    point_data, road_polygons = args
    point = Point(point_data['lon'], point_data['lat'])
    for i, road_polygon in enumerate(road_polygons):
        if road_polygon.contains(point):
            return (point_data['lon'], point_data['lat'], str(point_data['time']), i)
    return None


def plot_trajectories(trajectories, dict_data):
    colors = cm.rainbow(np.linspace(0, 1, len(dict_data)))
    args = []
    patches = [] #图例
    for i, (car_id, car_data) in enumerate(dict_data.items()):
        car_color = colors[i % len(colors)]  # 使用取模运算确保颜色索引不超出范围
        for point_data in car_data:
            args.append((point_data, trajectories))  # 传递一个元组，包含点数据和道路多边形列表
        patches.append(mpatches.Patch(color=car_color, label=car_id))

    with Pool() as p:
        for result in tqdm(p.imap(check_point_on_road, args), total=len(args)):
            if result is not None:
                lon, lat, time, i = result
                ax.scatter(lon, lat, color=colors[i % len(colors)])  # 使用取模运算确保颜色索引不超出范围

    plt.legend(handles=patches)




if __name__ == "__main__":
    file = './路网数据/东三环北路.txt'
    with open(file, 'r') as f:
        data = eval(f.read())

    readtxt('log-temp.txt')

    fig, ax = plt.subplots(figsize=(10, 8))

    road_polygons = [create_road_polygon(trajectory) for trajectory in data]

    for trajectory in data:
        plot_road(trajectory)

    plot_trajectories(road_polygons, dict_data)

    plt.axis('equal')
    plt.show()
