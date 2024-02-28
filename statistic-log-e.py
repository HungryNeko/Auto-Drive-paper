import os
from shapely.geometry import Point, LineString
from pyproj import CRS, Transformer

def check_point_on_road(point_data, trajectories, i, buffer_size=0.0002):
    point = Point(point_data['lon'], point_data['lat'])
    for trajectory in trajectories:
        road = LineString(trajectory)
        if road.buffer(0.0002).contains(point): # 使用指定的缓冲区大小
            return (point_data['lon'], point_data['lat'], str(point_data['time']), i)
    return None

def process_file(input_file, output_file, road_coords):
    try:
        total_lines = sum(1 for line in open(input_file))  # 获取总行数
        with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
            for i, line in enumerate(f_in, 1):
                id, lon, lat = line.strip().split(',')
                car = {'lon': float(lon), 'lat': float(lat)}
                result = check_point_on_road(car, road_coords, i)
                if result is not None:
                    f_out.write(','.join(result) + '\n')
                # 计算剩余行数并显示
                remaining_lines = total_lines - i
                print(f"\rProcessing: Line {i}/{total_lines}, Remaining: {remaining_lines}", end='', flush=True)
            print("\nProcessing complete.")
    except Exception as e:
        print(f"\nError processing file '{input_file}': {e}")


if __name__ == '__main__':
    # 道路坐标文件路径 (北三环.txt)
    road_data_file = '路网数据/北三环.txt'
    with open(road_data_file, 'r') as f:
        road_coords = eval(f.read())
    road_coords = [coord for sublist in road_coords for coord in sublist]

    # 输入和输出文件路径
    input_file = 'log-E.txt'
    output_file = 'log-S.txt'

    # 处理输入文件并将筛选后的点保存到输出文件
    process_file(input_file, output_file, road_coords)
