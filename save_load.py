import json
import datetime

from tqdm import tqdm


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

def savedata(data, filepath):
    if not isinstance(data, list):
        data = [data]  # 如果数据不是列表，将其包装在列表中
    with open(filepath, 'a') as f:
        for entry in data:
            json.dump(entry, f, cls=DateTimeEncoder)
            f.write('\n')



import json

def loaddata(filepath):
    loaded_data = []
    with open(filepath, 'r') as f:
        for line in f:
            try:
                # 尝试解析带有双引号的 JSON 字符串
                entry = json.loads(line.strip())
                loaded_data.append(entry)
            except json.JSONDecodeError:
                try:
                    # 如果解析失败，尝试解析带有单引号的 JSON 字符串
                    entry = json.loads(line.strip().replace("'", '"'))
                    loaded_data.append(entry)
                except Exception as e:
                    #print(f"加载数据时出错：{e}")
                    pass
    return loaded_data


def convert_data(loaded_data, full=False, limit=False):
    dict_data = {}
    count = 0
    for entry in tqdm(loaded_data, desc="Converting data"):
        count += 1
        try:
            lon, lat = float(entry['longitude']), float(entry['latitude'])
            gcj = []


            if full:
                dict_data.setdefault(entry['id'], []).append({
                    'id': entry['id'],
                    'time': datetime.datetime.strptime(entry['time'], "%Y-%m-%d %H:%M:%S"),
                    'lon': lon,
                    'lat': lat,
                    'speed': float(entry['speed']),
                    'acceleration': float(entry['acceleration']),
                    'angle': float(entry['angle'])
                })
            else:
                dict_data.setdefault(entry['id'], []).append({
                    'id': entry['id'],
                    'time': datetime.datetime.strptime(entry['time'], "%Y-%m-%d %H:%M:%S"),
                    'lon': lon,
                    'lat': lat
                })
        except Exception as e:
            # print(f"Error while processing entry: {entry}")
            # print(e)
            continue
        if limit and count == limit:
            break

    return dict_data



def cleandata(filepath):
    try:
        with open(filepath, 'w') as f:
            f.truncate(0)
        print(f"文件 '{filepath}' 已成功清空。")
    except Exception as e:
        print(f"清空文件 '{filepath}' 内容时出现错误：{e}")

# 测试数据
test_data = [
    {'id': 1, 'time': datetime.datetime(2008, 2, 5, 17, 21, 21), 'lon': 116.43465281165018, 'lat': 39.90914907074822, 'speed': 2.7397531491920715, 'acceleration': 0.0036810899982913964, 'angle': 189.49793934552773},
    {'id': 2, 'time': datetime.datetime(2008, 2, 5, 18, 30, 15), 'lon': 116.43465281165018, 'lat': 39.90914907074822, 'speed': 2.7397531491920715, 'acceleration': 0.0036810899982913964, 'angle': 189.49793934552773},
    {'id': 3, 'time': datetime.datetime(2008, 2, 5, 19, 45, 38), 'lon': 116.43465281165018, 'lat': 39.90914907074822, 'speed': 2.7397531491920715, 'acceleration': 0.0036810899982913964, 'angle': 189.49793934552773}
]
t={'id': 1, 'time': datetime.datetime(2008, 2, 5, 17, 21, 21), 'lon': 116.43465281165018, 'lat': 39.90914907074822, 'speed': 2.7397531491920715, 'acceleration': 0.0036810899982913964, 'angle': 189.49793934552773}
if __name__ == "__main__":
    # 将数据保存到文件
    cleandata('testdata.txt')
    savedata(t, 'testdata.txt')

    # 从文件中加载数据
    loaded_data = loaddata('data东四环中路.txt')

    print(loaded_data)

