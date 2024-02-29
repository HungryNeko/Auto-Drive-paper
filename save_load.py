import json
import datetime

def savedata(data, filepath):
    with open(filepath, 'a') as f:
        for entry in data:
            json.dump(entry, f)
            f.write('\n')

def loaddata(filepath):
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            entry = json.loads(line)
            data.append(entry)
    return data
