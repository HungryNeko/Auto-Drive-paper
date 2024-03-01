from datetime import datetime, timedelta
import save_load

def count_data_in_time_segments(data, segment_size):
    # 计算数据中的最早时间和最晚时间
    min_time = min(entry["time"] for entry in data)
    max_time = max(entry["time"] for entry in data)

    # 将时间字符串转换为 datetime 对象
    min_time_obj = datetime.fromisoformat(min_time)
    max_time_obj = datetime.fromisoformat(max_time)

    # 初始化时间段字典
    time_segments = {}

    # 遍历数据并计算每个时间段内的数据条数
    current_time = min_time_obj
    while current_time <= max_time_obj:
        end_time = current_time + timedelta(minutes=segment_size)
        count = sum(1 for entry in data if current_time <= datetime.fromisoformat(entry["time"]) < end_time)
        time_segments[(current_time, end_time)] = count
        current_time = end_time

    # 找到数据量最多的时间段
    most_common_segment = max(time_segments, key=time_segments.get)
    most_common_count = time_segments[most_common_segment]

    # 返回数据量最多的时间段和对应的数据量
    return most_common_segment, most_common_count

def save_data_in_time_segment(data, segment, filename_prefix):
    # 打开文件，准备写入数据
    filename = f"{filename_prefix}_in_{segment_size}min.txt"
    with open(filename, 'w') as f:
        # 遍历数据，将在最多数据量时间段内的数据写入文件
        for entry in data:
            entry_time = datetime.fromisoformat(entry["time"])
            if segment[0] <= entry_time < segment[1]:
                f.write(str(entry) + '\n')

    print(f"数据已保存到文件：{filename}")

if __name__ == "__main__":
    # 加载数据
    data = save_load.loaddata("data东四环中路.txt")

    # 设置时间段大小（分钟）
    segment_size = 10

    # 统计数据在每个时间段内的条数，找到数据量最多的时间段
    most_common_segment, most_common_count = count_data_in_time_segments(data, segment_size)

    # 将数据保存到数据量最多的时间段文件中
    save_data_in_time_segment(data, most_common_segment, "data东四环中路_segmented")
    print("数据量最多的时间段：", most_common_segment)
    print("数据量：", most_common_count)
