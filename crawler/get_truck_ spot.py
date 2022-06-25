import pandas as pd
from MySQL import MySQL

Taipei_car_move = pd.read_csv("https://data.taipei/api/dataset/6bb3304b-4f46-4bb0-8cd1-60c66dcd1cae/resource/649d4ef4-e90c-445d-8aa7-bbc0cd7a056f/download",encoding="ANSI")
# print(Taipei_car_move)
for row in range(len(Taipei_car_move)):
    address = Taipei_car_move["地點"][row]
    arrive_time = Taipei_car_move["抵達時間"]
    print(Taipei_car_move["經度"]
    print(Taipei_car_move["緯度"])

New_Taipei_car_move = pd.read_csv("https://data.ntpc.gov.tw/api/datasets/EDC3AD26-8AE7-4916-A00B-BC6048D19BF8/csv/file")
# print(New_Taipei_car_move)