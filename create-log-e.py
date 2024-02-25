"""
重新创建log-e，包含所有的坐标和id，不做额外计算
"""
import os

folder_path = '../taxi_log_2008_by_id'

def extract_data(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                elements = line.strip().split(",")
                if len(elements) >= 4:  # 确保数据包含id、经度和纬度
                    id = elements[0]
                    time=elements[1]
                    longitude = elements[2]
                    latitude = elements[3]
                    if id and longitude and latitude and time:  # 确保数据非空
                        yield f"{id},{time},{longitude},{latitude}"
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        pass

def process_file(file_name):
    log_entries = []
    file_path = os.path.join(folder_path, file_name)
    for data_entry in extract_data(file_path):
        log_entries.append(data_entry)
    if log_entries:
        with open('log-E.txt', 'a') as log_file:
            log_file.write('\n'.join(log_entries) + '\n')

def read_all_files():
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        if file_name.endswith('.txt'):
            process_file(file_name)

if __name__ == "__main__":
    with open('log-E.txt', 'w'): pass
    read_all_files()

