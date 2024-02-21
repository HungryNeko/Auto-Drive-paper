import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
from pyproj import CRS, Transformer
from read import readtxt, dict_data
from multiprocessing import Pool
from tqdm import tqdm
from functools import partial

def is_vehicle_on_road(vehicle_coords, road_coords, lane_width=11.25):
    transformer = Transformer.from_crs(CRS('EPSG:4326'), CRS('EPSG:3857'), always_xy=True)
    vehicle_coords_proj = transformer.transform(*vehicle_coords)
    road_coords_proj = [transformer.transform(*road_coord) for road_coord in road_coords]
    vehicle_point = Point(vehicle_coords_proj)
    road_line = LineString(road_coords_proj)
    distance = vehicle_point.distance(road_line)
    return distance <= lane_width

def process_data(car, road_coords):
    if is_vehicle_on_road((car['lon'], car['lat']), road_coords):
        return car

def plot_on_road_points(ax, on_road_data):
    unique_car_ids = set(car['car_id'] for car in on_road_data)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_car_ids)))  # 生成彩虹颜色
    color_dict = dict(zip(unique_car_ids, colors))  # 创建一个字典，将车辆ID和颜色对应起来
    added_labels = set()  # 用于存储已经添加过的图例
    for car in on_road_data:
        lon, lat = car['lon'], car['lat']
        car_id = car['car_id']
        color = color_dict[car_id]  # 根据车辆ID获取颜色
        label = f"Car {car_id}" if car_id not in added_labels else ""  # 如果已经添加过图例，则不再添加
        ax.scatter(lon, lat, marker='o', color=color, label=label)
        added_labels.add(car_id)  # 将车辆ID添加到已添加的图例中

    ax.legend()


if __name__ == "__main__":
    file = './路网数据/北三环东路.txt'
    with open(file, 'r') as f:
        road_coords = eval(f.read())

    road_coords = [coord for sublist in road_coords for coord in sublist]

    readtxt('E:/Studyproject/re/log.txt')#完整的log

    # 用于存储符合条件的数据
    filtered_data = []

    with Pool() as pool:
        for car_id, car_list in tqdm(dict_data.items(), desc='Processing Data'):
            for car in car_list:
                car['car_id'] = car_id  # 添加车辆ID字段
                if is_vehicle_on_road((car['lon'], car['lat']), road_coords):
                    # 符合条件的数据，将其加入 filtered_data
                    filtered_data.append(car)

    # 使用进程处理数据
    with Pool() as pool:
        process_data_partial = partial(process_data, road_coords=road_coords)
        on_road_data = list(tqdm(pool.imap(process_data_partial, filtered_data), desc='Processing Data', total=len(filtered_data)))

    # 绘制在路上的点
    fig, ax = plt.subplots(figsize=(10, 8))

    # 绘制道路
    road_coords = np.array(road_coords)
    ax.plot(road_coords[:, 0], road_coords[:, 1], color='black', label='Road')

    # 绘制在路上的点
    plot_on_road_points(ax, on_road_data)

    # 设置图例
    ax.legend().set_visible(False)

    # 输出点在这条路上的总数
    num_cars = len(dict_data)
    total_points_on_road = len(on_road_data)
    num_cars_on_road = len(set(car['car_id'] for car in on_road_data))  # 计算在路上的车辆数量
    print(f"Number of cars in the dataset: {num_cars}")
    print(f"Total points on the road: {total_points_on_road}")
    print(f"Number of cars on the road: {num_cars_on_road}")  # 输出在路上的车辆数量

    plt.show()