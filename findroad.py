import threading
import numpy as np
from tqdm import tqdm
from sklearn.neighbors import BallTree
from calculation import distanceCal
from read import readtxt, readroad, road_info_dict, dict_data

readtxt('log.txt')
readroad()

earth_radius_km = 6371.393
num = 5
dist = 50

# Precompute distances and indices for all roads
road_coordinates = np.array([[road['avglon'], road['avglat']] for road in road_info_dict.values()])
ball_tree = BallTree(road_coordinates, metric='haversine')

car_info_with_path = {}
num_threads = 32

def process_vehicle_data(start, end, thread_id, pbar):
    thread_data = {}
    for i, (car_id, car_data_list) in enumerate(list(dict_data.items())[start:end], start=1):
        car_info_list = []
        for car_data in car_data_list:
            lon = car_data['lon']
            lat = car_data['lat']
            distances, indices = ball_tree.query(np.array([[lon, lat]]), num)
            valid_indices = [idx for idx, distance in zip(indices[0], distances[0]) if distance < dist]

            if valid_indices:
                nearest_road_ids = [list(road_info_dict.keys())[idx] for idx in valid_indices]

                min_distance = float('inf')
                nearest_road_id = None

                for road_id in nearest_road_ids:
                    road = road_info_dict[road_id]
                    road_coordinates = road['coordinates'][0]

                    for coords in road_coordinates:
                        road_lon, road_lat = coords[0], coords[1]
                        temp_distance = distanceCal(road_lon, road_lat, lon, lat)

                        if temp_distance < min_distance:
                            min_distance = temp_distance
                            nearest_road_id = road_id

                car_info = {
                    'time': car_data['time'].strftime("%Y-%m-d %H:%M:%S"),
                    'lon': lon,
                    'lat': lat,
                    'speed': car_data['speed'],
                    'acceleration': car_data['acceleration'],
                    'angle': car_data['angle'],
                    'nearest_road_id': nearest_road_id,
                    'nearest_road_name': road_info_dict[nearest_road_id]['name']
                }
                car_info_list.append(car_info)

        thread_data[car_id] = car_info_list
        pbar.update(1)

    car_info_with_path[thread_id] = thread_data

def run_threads():
    threads = []
    total_data = len(dict_data)
    chunk_size = total_data // num_threads

    with tqdm(total=total_data, desc="Processing Vehicles") as pbar:
        for i in range(num_threads):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i != num_threads - 1 else total_data
            thread = threading.Thread(target=process_vehicle_data, args=(start, end, i, pbar))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

run_threads()

# Combine results from all threads into final_car_info_with_path
final_car_info_with_path = {}
for thread_data in car_info_with_path.values():
    final_car_info_with_path.update(thread_data)

# Save the result to log1.txt
with open('log1.txt', 'w', encoding="utf-8", buffering=8192) as log_file:
    for car_id, car_info_list in final_car_info_with_path.items():
        for car_info in car_info_list:
            log_file.write(
                f"{car_id},{car_info['time']},{car_info['speed']},{car_info['acceleration']},{car_info['angle']},{car_info['lon']},{car_info['lat']},{car_info['nearest_road_id']},{car_info['nearest_road_name']}\n"
            )
