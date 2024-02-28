"""
change all coordinates in log-E and store in log-gcj
"""
import warnings

# 忽略特定类型的警告
warnings.filterwarnings("ignore")

from multiprocessing import Pool, cpu_count, freeze_support
from pyproj import Proj, transform
from tqdm import tqdm

def wgs84_to_gcj02(longitude, latitude):
    wgs84 = Proj(init='epsg:4326')  # WGS84坐标系
    gcj02 = Proj(init='epsg:4490')  # GCJ02坐标系
    gcj_longitude, gcj_latitude = transform(wgs84, gcj02, longitude, latitude)
    return gcj_longitude, gcj_latitude

def process_line(line):
    parts = line.strip().split(",")
    id_, timestamp, longitude, latitude = parts[0], parts[1], float(parts[2]), float(parts[3])
    gcj_longitude, gcj_latitude = wgs84_to_gcj02(longitude, latitude)
    return f"{id_},{timestamp},{gcj_longitude},{gcj_latitude}\n"

if __name__ == '__main__':
    freeze_support()

    input_file = "log-E.txt"
    output_file = "log-gcj.txt"

    # 获取推荐的进程数，即 CPU 的核心数
    recommended_processes = cpu_count()

    # 手动设置进程数，你可以根据需要修改这个值
    processes = min(recommended_processes, 8)  # 这里设置为推荐进程数和4之间的较小值

    with open(input_file, "r") as f_in:
        lines = f_in.readlines()

    with Pool(processes=processes) as pool:
        with open(output_file, "w") as f_out:
            for result in tqdm(pool.imap(process_line, lines), desc="Converting coordinates", total=len(lines), unit=" lines"):
                f_out.write(result)

    print("转换完成，并已保存到", output_file)

