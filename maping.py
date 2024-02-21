import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
from pyproj import CRS, Transformer
from read import readtxt, dict_data
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor


def is_vehicle_on_road_parallel(car, road_coords, lane_width=11.25):
    lon, lat = car['lon'], car['lat']

    # Assuming EPSG:4326 for lon/lat and EPSG:3857 for projected coordinates
    transformer = Transformer.from_crs(CRS('EPSG:4326'), CRS('EPSG:3857'), always_xy=True)

    # Make sure to pass both lon and lat to the transform method
    vehicle_coords_proj = transformer.transform(lon, lat)
    road_coords_proj = [transformer.transform(coord[0], coord[1]) for coord in road_coords]

    vehicle_point = Point(vehicle_coords_proj)
    road_line = LineString(road_coords_proj)

    distance = vehicle_point.distance(road_line)
    return distance <= lane_width


if __name__ == '__main__':
    file = './路网数据/北三环东路.txt'
    with open(file, 'r') as f:
        road_coords = eval(f.read())
    road_coords = [coord for sublist in road_coords for coord in sublist]

    readtxt('log.txt')

    # 用于存储符合条件的数据
    filtered_data = []

    # 使用并行加速
    with ProcessPoolExecutor() as executor:
        for car_list in tqdm(dict_data.values(), desc="Processing cars"):
            # 将is_vehicle_on_road_parallel函数应用于car_list中的每个car
            result = list(executor.map(is_vehicle_on_road_parallel, car_list, [road_coords] * len(car_list)))
            # 将符合条件的车辆数据加入filtered_data
            filtered_data.extend([car for car, is_on_road in zip(car_list, result) if is_on_road])

    # Convert filtered_data to a DataFrame
    df_filtered_data = pd.DataFrame(filtered_data)

    # Create a single figure with subplots
    fig, axes = plt.subplots(3, 1, figsize=(8, 12))

    # Plot speed distribution
    sns.histplot(df_filtered_data['speed'], stat="count", kde=True, color='blue', bins=30, ax=axes[0])
    axes[0].set_title('Speed Distribution')

    # Plot acceleration distribution
    sns.histplot(df_filtered_data['acceleration'], stat="count", kde=True, color='green', bins=30, ax=axes[1])
    axes[1].set_title('Acceleration Distribution')

    # Plot angle distribution
    sns.histplot(df_filtered_data['angle'], stat="count", kde=True, color='orange', bins=30, ax=axes[2])
    axes[2].set_title('Angle Distribution')

    # Adjust spacing between subplots
    plt.subplots_adjust(hspace=0.5)

    # Show the plot
    plt.show()
