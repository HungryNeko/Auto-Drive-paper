import json
import datetime
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

def savedata(data, filepath):
    with open(filepath, 'a') as f:
        for entry in data:
            json.dump(entry, f, cls=DateTimeEncoder)
            f.write('\n')

def loaddata(filepath):
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            entry = json.loads(line)
            data.append(entry)
    return data
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
if __name__ == "__main__":
    # 将数据保存到文件
    savedata(test_data, 'testdata.txt')

    # 从文件中加载数据
    loaded_data = loaddata('testdata.txt')

    print(loaded_data)
