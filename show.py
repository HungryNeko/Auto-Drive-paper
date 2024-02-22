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
import os

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


def plot_trajectories(trajectories):
    for trajectory in trajectories:
        coords = np.array(trajectory)
        ax.plot(coords[:, 0], coords[:, 1], '--', color='gray')  # 绘制中心线
        plot_road(coords, width=22.5, style='-', color='black')  # 绘制道路

# if __name__ == "__main__":
#     file = './路网数据/S50北五环.txt'
#     with open(file, 'r') as f:
#         data = eval(f.read())
#
#     #readtxt('log.txt')
#
#     fig, ax = plt.subplots(figsize=(10, 8))
#
#     # 绘制道路
#     plot_trajectories(data)
#
#     plt.show()


def plot_multiple_trajectories(directory):
    global  fig, ax
    # 遍历指定目录下的所有txt文件
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            # 创建新的图形对象和Axes对象
            fig, ax = plt.subplots(figsize=(10, 8))
            xlim = None
            ylim = None

            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                data = eval(f.read())

            # 找到所有轨迹中的最小和最大横纵坐标
            for trajectory in data:
                coords = np.array(trajectory)
                traj_xlim = [np.min(coords[:, 0]), np.max(coords[:, 0])]
                traj_ylim = [np.min(coords[:, 1]), np.max(coords[:, 1])]

                # 更新整体的横纵坐标范围
                if xlim is None:
                    xlim = traj_xlim
                else:
                    xlim = [min(xlim[0], traj_xlim[0]), max(xlim[1], traj_xlim[1])]

                if ylim is None:
                    ylim = traj_ylim
                else:
                    ylim = [min(ylim[0], traj_ylim[0]), max(ylim[1], traj_ylim[1])]

            # 计算纵横比例
            x_length = xlim[1] - xlim[0]
            y_length = ylim[1] - ylim[0]
            aspect_ratio = y_length / x_length

            # 设置横纵坐标范围
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)

            # 设置纵横比例
            ax.set_aspect(aspect_ratio)

            # 绘制道路
            plot_trajectories(data)

            # 显示图形
            plt.show()


# 使用示例
directory = './路网数据/'
plot_multiple_trajectories(directory)