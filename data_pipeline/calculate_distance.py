from scipy.spatial import distance
from MySQL import MySQL
import time
import os


def calculate_distance():
    id_list = []
    for house in MySQL.get_house_lat_lon():
        tuple_list = []
        house_id = house["house_id"]
        print(house_id)
        house_city_id = house["city_id"]
        id_list.append(house_id)
        house_location = (house["longitude"],house["latitude"])
        for spot in MySQL.get_truck_lat_lon():
            spot_id = spot["truck_spot_id"]
            spot_city_id = spot["city_id"]
            if house_city_id == spot_city_id:
                truck_location = (spot["longitude"],spot["latitude"])
                dis = distance.euclidean(house_location,truck_location)
                if dis < 0.02:
                    tuple = (house_id,spot_id,dis)
                    tuple_list.append(tuple)
                else:
                    pass
            else:
                pass
        MySQL.insert_distance_truck_house(tuple_list)
    MySQL.finish_update(id_list)
    print("Finished")
    os._exit(0)


if __name__ == "__main__":
    start = time.perf_counter()
    calculate_distance()
    end = time.perf_counter()
    print(end-start)