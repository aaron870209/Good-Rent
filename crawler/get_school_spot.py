import math
import pandas as pd
from MySQL import MySQL
from pymysql import IntegrityError


def school(tag):
    if tag == 1:
        school = pd.read_excel("109學年度各級學校分布位置_國小.xls")
    elif tag ==2:
        school = pd.read_excel("109學年度各級學校分布位置_國中.xls")
    elif tag == 3:
        school = pd.read_excel("109學年度各級學校分布位置_高中職.xls")
    else:
        school = pd.read_excel("109學年度各級學校分布位置_大專院校.xls")
    result_list = []
    for row in range(len(school)):
        address = school["地址"][row]
        name = school["學校名稱"][row]
        city = school["縣市別"][row]
        if city == "新北市" or city == "臺北市":
            X = school["X 坐標"][row]
            Y = school["Y 坐標"][row]
            latitude,longitude = twd97_to_lonlat(X, Y)
            if city == "新北市":
                city_id = 2
            else:
                city_id = 1
            print("address=",address," name=",name," city",city," longitude",longitude," latitude",latitude)
            tuple = (name, address, longitude, latitude, city_id)
            result_list.append(tuple)
    try:
        print(len(result_list))
        MySQL.insert_school_spot(result_list)
    except IntegrityError:
        pass


def twd97_to_lonlat(x, y):
    a = 6378137
    b = 6356752.314245
    long_0 = 121 * math.pi / 180.0
    k0 = 0.9999
    dx = 250000
    dy = 0
    e = math.pow((1-math.pow(b, 2)/math.pow(a,2)), 0.5)
    x -= dx
    y -= dy
    M = y / k0
    mu = M / ( a*(1-math.pow(e, 2)/4 - 3*math.pow(e,4)/64 - 5 * math.pow(e, 6)/256))
    e1 = (1.0 - pow((1   - pow(e, 2)), 0.5)) / (1.0 +math.pow((1.0 -math.pow(e,2)), 0.5))
    j1 = 3*e1/2-27*math.pow(e1,3)/32
    j2 = 21 * math.pow(e1,2)/16 - 55 * math.pow(e1, 4)/32
    j3 = 151 * math.pow(e1, 3)/96
    j4 = 1097 * math.pow(e1, 4)/512
    fp = mu + j1 * math.sin(2*mu) + j2 * math.sin(4* mu) + j3 * math.sin(6*mu) + j4 * math.sin(8* mu)
    e2 = math.pow((e*a/b),2)
    c1 = math.pow(e2*math.cos(fp),2)
    t1 = math.pow(math.tan(fp),2)
    r1 = a * (1-math.pow(e,2)) / math.pow( (1-math.pow(e,2)* math.pow(math.sin(fp),2)), (3/2))
    n1 = a / math.pow((1-math.pow(e,2)*math.pow(math.sin(fp),2)),0.5)
    d = x / (n1*k0)
    q1 = n1* math.tan(fp) / r1
    q2 = math.pow(d,2)/2
    q3 = ( 5 + 3 * t1 + 10 * c1 - 4 * math.pow(c1,2) - 9 * e2 ) * math.pow(d,4)/24
    q4 = (61 + 90 * t1 + 298 * c1 + 45 * math.pow(t1,2) - 3 * math.pow(c1,2) - 252 * e2) * math.pow(d,6)/720
    lat = fp - q1 * (q2 - q3 + q4)
    q5 = d
    q6 = (1+2*t1+c1) * math.pow(d,3) / 6
    q7 = (5 - 2 * c1 + 28 * t1 - 3 * math.pow(c1,2) + 8 * e2 + 24 * math.pow(t1,2)) * math.pow(d,5) / 120
    lon = long_0 + (q5 - q6 + q7) / math.cos(fp)
    lat = (lat*180) / math.pi
    lon = (lon*180) / math.pi
    return lat, lon


if __name__ == '__main__':
    school(1)
    school(2)
    school(3)
    school(4)