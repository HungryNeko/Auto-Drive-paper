"""
change all coordinates in log-E and store in log-gcj
"""
import os
import warnings

# 忽略特定类型的警告
warnings.filterwarnings("ignore")

from multiprocessing import Pool, cpu_count, freeze_support
from pyproj import Proj, transform
from tqdm import tqdm
import math
x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626 # π
a = 6378245.0 # 长半轴
ee = 0.00669342162296594323 # 扁率
def wgs84togcj02(lng,lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:列表
    """
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    #print([mglng, mglat])
    return [mglng, mglat]

def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
    math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
    math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret
def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

def process_line(line):
    parts = line.strip().split(",")
    id_, timestamp, longitude, latitude = parts[0], parts[1], float(parts[2]), float(parts[3])
    gcj_longitude, gcj_latitude = wgs84togcj02(longitude, latitude)
    return f"{id_},{timestamp},{gcj_longitude},{gcj_latitude}\n"
"""
转换单个文件
if __name__ == '__main__':
    freeze_support()

    input_file = "../01/6656.txt"
    output_file = "log-6656.txt"

    # 获取推荐的进程数，即 CPU 的核心数
    recommended_processes = cpu_count()

    # 手动设置进程数，你可以根据需要修改这个值
    processes = min(recommended_processes, 16)  # 这里设置为推荐进程数和4之间的较小值

    with open(input_file, "r") as f_in:
        lines = f_in.readlines()

    with Pool(processes=processes) as pool:
        with open(output_file, "w") as f_out:
            for result in tqdm(pool.imap(process_line, lines), desc="Converting coordinates", total=len(lines), unit=" lines"):
                f_out.write(result)

    print("转换完成，并已保存到", output_file)
"""
if __name__ == '__main__':
    freeze_support()

    input_directory = "../01/"
    output_directory = "01-c/"

    # 获取推荐的进程数，即 CPU 的核心数
    recommended_processes = cpu_count()

    # 手动设置进程数，你可以根据需要修改这个值
    processes = min(recommended_processes, 16)  # 这里设置为推荐进程数和4之间的较小值

    # 确保输出目录存在
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 获取01目录下所有文件
    input_files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]

    with Pool(processes=processes) as pool:
        for input_file in input_files:
            with open(os.path.join(input_directory, input_file), "r") as f_in:
                lines = f_in.readlines()

            output_file = os.path.join(output_directory, input_file)

            with open(output_file, "w") as f_out:
                for result in tqdm(pool.imap(process_line, lines), desc=f"Converting {input_file}", total=len(lines), unit=" lines"):
                    f_out.write(result)

            print(f"文件 {input_file} 转换完成，并已保存到 {output_file}")
