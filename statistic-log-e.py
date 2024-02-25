import os
from shapely.geometry import Point, LineString
from pyproj import CRS, Transformer

def is_vehicle_on_road(car, road_coords, lane_width=11.25):
    lon, lat = car['lon'], car['lat']

    # Assuming EPSG:4326 for lon/lat and EPSG:3857 for projected coordinates
    transformer = Transformer.from_crs(CRS('EPSG:4326'), CRS('EPSG:3857'), always_xy=True)

    # Transform vehicle coordinates to projected coordinates
    vehicle_coords_proj = transformer.transform(lon, lat)
    vehicle_point = Point(vehicle_coords_proj)

    # Convert road coordinates to projected coordinates
    road_coords_proj = [transformer.transform(coord[0], coord[1]) for coord in road_coords]
    road_line = LineString(road_coords_proj)

    # Check if the vehicle is within the specified lane width of the road
    distance = vehicle_point.distance(road_line)
    return distance <= lane_width

def process_file(input_file, output_file, road_coords):
    try:
        total_lines = sum(1 for line in open(input_file))  # 获取总行数
        with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
            for i, line in enumerate(f_in, 1):
                id, lon, lat = line.strip().split(',')
                car = {'lon': float(lon), 'lat': float(lat)}
                if is_vehicle_on_road(car, road_coords):
                    f_out.write(f"{id},{lon},{lat}\n")
                # 计算剩余行数并显示
                remaining_lines = total_lines - i
                print(f"\rProcessing: Line {i}/{total_lines}, Remaining: {remaining_lines}", end='', flush=True)
            print("\nProcessing complete.")
    except Exception as e:
        print(f"\nError processing file '{input_file}': {e}")


if __name__ == '__main__':
    # Path to the road coordinates file (北三环.txt)
    road_data_file = '路网数据/北三环.txt'
    with open(road_data_file, 'r') as f:
        road_coords = eval(f.read())
    road_coords = [coord for sublist in road_coords for coord in sublist]

    # Input and output file paths
    input_file = 'log-E.txt'
    output_file = 'log-S.txt'

    # Process the input file and save the filtered points to the output file
    process_file(input_file, output_file, road_coords)
