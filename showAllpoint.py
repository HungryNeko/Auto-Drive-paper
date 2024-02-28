import matplotlib.pyplot as plt
from tqdm import tqdm

# 读取文件
file_path = "log-E.txt"
with open(file_path, "r") as f:
    lines = f.readlines()

# 提取有效范围内的坐标信息
min_longitude, max_longitude = 116.20, 116.60
min_latitude, max_latitude = 39.75, 40.03
longitudes = []
latitudes = []
for line in tqdm(lines, desc="Processing lines", unit=" lines"):
    parts = line.strip().split(",")
    longitude = float(parts[2])
    latitude = float(parts[3])
    if (min_longitude <= longitude <= max_longitude) and (min_latitude <= latitude <= max_latitude):
        longitudes.append(longitude)
        latitudes.append(latitude)

# 绘制散点图，调整点的大小为1
plt.scatter(longitudes, latitudes, color='blue', marker='o', alpha=0.5, s=1)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Coordinates')

# 不设置坐标轴范围，使用实际经纬度
plt.grid(True)
plt.show()
