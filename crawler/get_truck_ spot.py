import pandas as pd
from pymysql import IntegrityError

from MySQL import MySQL


def Taipei_truck_spot():
    Taipei_car_move = pd.read_csv("https://data.taipei/api/dataset/6bb3304b-4f46-4bb0-8cd1-60c66dcd1cae/resource/649d4ef4-e90c-445d-8aa7-bbc0cd7a056f/download",encoding="ANSI")
    for row in range(len(Taipei_car_move)):
        address = Taipei_car_move["地點"][row]
        arrive_time = Taipei_car_move["抵達時間"][row]
        longitude = Taipei_car_move["緯度"][row]
        latitude = Taipei_car_move["經度"][row]
        dict = {"address":address, "arrive_time":arrive_time,"longitude":longitude,"latitude":latitude,"city_id":1}
        try:
            MySQL.insert_truck_spot_to_SQL(dict)
        except IntegrityError:
            pass


def New_Taipei_truck_spot():
    New_Taipei_car_move = pd.read_csv("https://data.ntpc.gov.tw/api/datasets/EDC3AD26-8AE7-4916-A00B-BC6048D19BF8/csv/file")
    for row in range(len(New_Taipei_car_move)):
        address = New_Taipei_car_move["name"][row]
        arrive_time = New_Taipei_car_move["time"][row]
        longitude = New_Taipei_car_move["longitude"][row]
        latitude = New_Taipei_car_move["latitude"][row]
        dict = {"address":address, "arrive_time":arrive_time,"longitude":longitude,"latitude":latitude,"city_id":2}
        try:
            MySQL.insert_truck_spot_to_SQL(dict)
        except IntegrityError:
            pass


if __name__ == "__main__":
    Taipei_truck_spot()
    New_Taipei_truck_spot()