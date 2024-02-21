from shapely.geometry import Point, Polygon

# 五环的坐标点，这里只是示例，你需要替换成实际的坐标点
#la and longitude
coords1 = [(40.012182,116.273565), (40.003809,116.267839),(39.994667,116.223981),(39.877826,116.206952),(39.777582,116.275071),(39.775535,116.372113),(39.758862,116.378962),(39.770855,116.422726),(39.787233,116.430718),(39.792261,116.464465),(39.811857,116.483595),(39.852143,116.549799),(39.941696,116.542286),(40.013708,116.484133),(40.021667,116.437477)]
#la->lon lon->la
coords = [(lon, lat) for lat, lon in coords1]

# 创建一个Polygon对象
polygon = Polygon(coords)

def carIsIn5(lon,lat):
    point=Point(lon,lat)
    if polygon.contains(point):
        return True
    else:
        return False
    # 检查每个出租车的坐标
