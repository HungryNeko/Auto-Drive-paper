import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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

def check_point_on_road(args):
    point_data, trajectories, i = args
    point = Point(point_data['lon'], point_data['lat'])
    for trajectory in trajectories:
        road = LineString(trajectory)
        if road.buffer(0.0001).contains(point):  # Adjust the buffer size as needed
            return (point_data['lon'], point_data['lat'], str(point_data['time']), i)
    return None

def plot_distribution(dict_data, fields):
    fig, axs = plt.subplots(len(fields), 1, figsize=(10, 8))
    for ax, field in zip(axs, fields):
        data = []
        for car_id, car_data in tqdm(dict_data.items(), desc=f'Processing {field}'):
            for point_data in car_data:
                data.append(point_data[field])
        sns.histplot(data, bins=30, kde=True, ax=ax)
        ax.set_title(f'Distribution of {field}')
        ax.set_xlabel(field)
        ax.set_ylabel('Frequency')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    file = './路网数据/东二环.txt'
    with open(file, 'r') as f:
        data = eval(f.read())

    readtxt('log.txt')

    plot_distribution(dict_data, ['speed', 'acceleration', 'angle'])
