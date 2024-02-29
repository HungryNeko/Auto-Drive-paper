from datetime import datetime
from collections import defaultdict
import save_load
# 示例数据
data=save_load.loaddata("data东四环中路.txt")
print(data)
minute_counts = {}

# 遍历数据，统计每个分钟出现的次数
for entry in data:
    time_str = entry["time"]
    time_obj = datetime.fromisoformat(time_str)
    # 只保留分钟部分，将秒和微秒都置为0
    minute = time_obj.replace(second=0, microsecond=0)
    # 如果这个分钟已经在字典中，则将计数加1；否则，将计数设置为1
    minute_counts[minute] = minute_counts.get(minute, 0) + 1

# 找到出现次数最多的分钟和对应的次数
most_common_minute = max(minute_counts, key=minute_counts.get)
most_common_count = minute_counts[most_common_minute]

print("出现次数最多的一分钟：", most_common_minute)
print("次数：", most_common_count)