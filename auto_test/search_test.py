import requests
import json
import os
from datetime import date
from dotenv import load_dotenv
import datetime
load_dotenv()
from pymysqlpool.pool import Pool
today = date.today()
yesterday = today-datetime.timedelta(days=1)
houses = [273767,345517]
pool = Pool(host=os.getenv("host"), user=os.getenv("user"), password=os.getenv("password"), db=os.getenv("database"),
            charset='utf8mb4')
pool.init()
connection = pool.get_conn()
cursor = connection.cursor()
cursor.execute(
    f"UPDATE house set `date`='{str(yesterday)}' where house_id IN {tuple(houses)}"
)
connection.commit()


def test_ajax():
    api = "http://localhost:3000/search"
    request = {'data': {'taipei': ['信義區', '士林區', '內湖區'], 'new_taipei': [], 'type': ['獨立套房'], 'rent': ['5000元~10000元']}, 'page': 0,"test":1}
    response = requests.post(api,json.dumps(request).encode('utf-8'))
    assert response.json() == {'data': [{'address': '內湖區環山路一段60巷', 'city': '臺北市', 'city.city_id': 1, 'city_id': 1, 'date': '2022-07-20', 'floor': '5', 'house_id': 273767, 'house_type': '獨立套房', 'img': 'https://img1.591.com.tw/house/2010/05/20/127434252127214802.jpg!510x400.jpg', 'key': '內湖區環山路一段60巷獨立套房6坪5', 'latitude': 25.0871, 'longitude': 121.566, 'price': 10000, 'size': '6坪', 'tag': '屋主直租 近捷運 新上架 拎包入住 隨時可遷入', 'title': '西湖捷運站旁,獨立洗衣機,有陽台及對外窗', 'type.type_id': 2, 'type_id': 2, 'update': 1, 'url': 'https://rent.591.com.tw/rent-detail-12944345.html'},
                                        {'address': '士林區菁山路', 'city': '臺北市', 'city.city_id': 1, 'city_id': 1, 'date': '2022-07-20', 'floor': 'B1/5', 'house_id': 345517, 'house_type': '獨立套房', 'img': 'https://img2.591.com.tw/house/2022/07/20/165829152525705804.jpg!510x400.jpg', 'key': '士林區菁山路獨立套房2.5坪B1/5', 'latitude': 25.1414, 'longitude': 121.568, 'price': 7500, 'size': '2.5坪', 'tag': '新上架 隨時可遷入', 'title': '文化大學套房出租', 'type.type_id': 2, 'type_id': 2, 'update': 1, 'url': 'https://rent.591.com.tw/rent-detail-12946370.html'}] ,'page': 0, 'total':2}

def test_ajax_newtaipei():
    api = "http://localhost:3000/search"
    request = {'data': {'taipei': ['信義區', '士林區', '內湖區'], 'new_taipei': [], 'type': ['獨立套房'], 'rent': ['5000元~10000元']}, 'page': 0,"test":1}
    response = requests.post(api,json.dumps(request).encode('utf-8'))
    assert response.json() == {'data': [{'address': '內湖區環山路一段60巷', 'city': '臺北市', 'city.city_id': 1, 'city_id': 1, 'date': '2022-07-20', 'floor': '5', 'house_id': 273767, 'house_type': '獨立套房', 'img': 'https://img1.591.com.tw/house/2010/05/20/127434252127214802.jpg!510x400.jpg', 'key': '內湖區環山路一段60巷獨立套房6坪5', 'latitude': 25.0871, 'longitude': 121.566, 'price': 10000, 'size': '6坪', 'tag': '屋主直租 近捷運 新上架 拎包入住 隨時可遷入', 'title': '西湖捷運站旁,獨立洗衣機,有陽台及對外窗', 'type.type_id': 2, 'type_id': 2, 'update': 1, 'url': 'https://rent.591.com.tw/rent-detail-12944345.html'},
                                        {'address': '士林區菁山路', 'city': '臺北市', 'city.city_id': 1, 'city_id': 1, 'date': '2022-07-20', 'floor': 'B1/5', 'house_id': 345517, 'house_type': '獨立套房', 'img': 'https://img2.591.com.tw/house/2022/07/20/165829152525705804.jpg!510x400.jpg', 'key': '士林區菁山路獨立套房2.5坪B1/5', 'latitude': 25.1414, 'longitude': 121.568, 'price': 7500, 'size': '2.5坪', 'tag': '新上架 隨時可遷入', 'title': '文化大學套房出租', 'type.type_id': 2, 'type_id': 2, 'update': 1, 'url': 'https://rent.591.com.tw/rent-detail-12946370.html'}] ,'page': 0, 'total':2}

