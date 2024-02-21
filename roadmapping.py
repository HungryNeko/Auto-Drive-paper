import sys
import os
import matplotlib.pyplot as plt
from rtree import index
from geopy.distance import geodesic

def main(name, args):
    array = args.replace('"', '').split('|')  # 删除所有的双引号

    point_counter = 0  # 用于跟踪点的序号
    for i in range(len(array)):
        original = array[i]
        for j in range(len(array)):
            originalArray = original.split('_')
            compare = array[j]
            compareArray = compare.split('_')
            if originalArray[0] == compareArray[-1]:
                originalNew = originalArray[1:]  # 删除连接部分
                array[i] = '@@@@@'
                array[j] = compare + '_' + '_'.join(originalNew)

    while '@@@@@' in array:
        array.remove('@@@@@')

    result = []
    for i in range(len(array)):
        locationArray = []
        locationStrArray = array[i].split('_')
        for item in locationStrArray:
            lnglat = item.split(',')
            locationArray.append([float(lnglat[0]), float(lnglat[1])])
        result.append(locationArray)

        x = [point[0] for point in locationArray]
        y = [point[1] for point in locationArray]

        # 在点的周围添加序号
        # for xx, yy in zip(x, y):
        #     plt.text(xx, yy, str(point_counter), fontsize=7, ha='center', va='bottom', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
        #     point_counter += 1

        plt.plot(x, y)

    print(name)
    # plt.xlabel('Longitude')
    # plt.ylabel('Latitude')
    # plt.show()
    return result

def build_rtree(coordinates):
    p = index.Property()
    p.dimension = 2  # 设置维度为2
    rtree_idx = index.Index(properties=p)

    for i, locationArray in enumerate(coordinates):
        if isinstance(locationArray, list) and len(locationArray) >= 2:
            for lon, lat in locationArray:
                rtree_idx.insert(i, (lon, lat, lon, lat))  # 使用(minx, miny, maxx, maxy)形式插入点

    return rtree_idx


def test_rtree_index(rtree_idx):
    # 选择一些测试坐标
    test_coordinates = [
        (longitude, latitude) for longitude, latitude in [
            (116.442489, 39.965757),
            # 添加更多测试坐标
        ]
    ]

    # 查询测试坐标
    for coord in test_coordinates:
        result = list(rtree_idx.intersection((coord[0], coord[1], coord[0], coord[1])))
        print(f"Querying coordinates {coord}: Found points at indices {result}")

def is_point_near_lines(point, rtree_idx, distance_threshold):
    lon, lat = point

    # 构建查询矩形
    query_rect = (lon - 0.00001, lat - 0.00001, lon + 0.00001, lat + 0.00001)

    # 查询附近的线段
    nearby_lines = list(rtree_idx.intersection(query_rect))

    # 将距离阈值从米转换为经纬度的差异
    distance_threshold_km = distance_threshold / 1000.0

    # 判断每个线段是否在指定距离范围内
    for line_index in nearby_lines:
        line_coordinates = coordinates[line_index]

        for line_lon, line_lat in line_coordinates:
            # 使用 geopy 计算实际距离
            actual_distance = geodesic((lat, lon), (line_lat, line_lon)).meters

            # 判断是否在指定距离范围内
            if actual_distance <= distance_threshold:
                return True

    return False

# def read_coordinates_from_file(file_path):
#     print("read_coordinates_from_file")
#     with open(file_path, 'r') as log_file:
#         log_lines = log_file.readlines()

#     coordinates = []
#     for line in log_lines:
#         #print(line)  # 添加这行打印语句
#         # 解析每行代码，提取坐标信息
#         parts = line.strip().split(',')
#         if len(parts) >= 6:
#             lon, lat = map(float, parts[-2:])
#             coordinates.append((lon, lat))

#     return coordinates


# def readfile(log_file_path, output_file_path):
#     # 读取坐标信息
#     coordinates = read_coordinates_from_file(log_file_path)
#     print(coordinates)
#     # 建立 R-tree
#     rtree_idx = build_rtree(coordinates)

#     # 测试每个坐标是否在附近，如果是则保存整行代码到 choose.txt
#     print("write file")
#     with open(log_file_path, 'r') as log_file, open(output_file_path, 'w') as output_file:
#         for line_num, line in enumerate(log_file, start=1):
#             try:
#                 parts = line.strip().split(',')
#                 if len(parts) >= 2:
#                     lon, lat = map(float, parts[-2:])
#                     #print(lon, lat)
#                     if is_point_near_lines((lon, lat), rtree_idx, distance_threshold=1000.0):
#                         print("!!!!!!!!!!!!!!!!!!!!")
#                         output_file.write(line)
#                         print(line)
#                 else:
#                     print(f"第 {line_num} 行缺少坐标信息或格式不正确：{line}")
#             except ValueError:
#                 print(f"第 {line_num} 行坐标信息格式不正确：{line}")
#             except Exception as e:
#                 print(f"第 {line_num} 行发生异常：{e}，行内容：{line}")

if __name__ == '__main__':
    path = './'
    files = os.listdir(path)
    file='北京市五环路网数据/北三环东路.txt'
    with open(file, 'r') as f:
        args = f.read()
    result = main(file, args)
    coordinates = result
    rtree_idx=build_rtree(result)
    test_rtree_index(rtree_idx)

    test_coordinates = [
            (116.442489, 39.965757),  #gpt（高德上的东北三环） 在第一个线段附近
            (116.445325,39.974078),#百度的东北三环
            (116.433475,39.969274),#高德的东北三环
            (116.44386,39.964855),#gaode
            (116.447489, 39.965757)   # 不在任何线段附近
        ]

    # 查询测试坐标
    for coord in test_coordinates:
        result = is_point_near_lines(coord, rtree_idx, distance_threshold=1.0)
        print(f"Querying coordinates {coord}: Found nearby lines: {result}")
    # log_file_path = 'log.txt'  # 修改为你的 log 文件路径
    # output_file_path = 'choose.txt'
    # readfile(log_file_path, output_file_path)

