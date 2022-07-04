from scipy.spatial import distance
from MySQL import MySQL
import time


def calculate_distance():
    for house in MySQL.get_house_lat_lon():
        tuple_list = []
        house_id = house["house_id"]
        print(house_id)
        house_city_id = house["city_id"]
        house_location = (house["longitude"],house["latitude"])
        for spot in MySQL.get_school_lat_lon():
            spot_id = spot["school_id"]
            spot_city_id = spot["city_id"]
            if house_city_id == spot_city_id:
                school_location = (spot["longitude"],spot["latitude"])
                dis = distance.euclidean(house_location,school_location)
                if dis < 0.02:
                    tuple = (house_id,spot_id,dis)
                    tuple_list.append(tuple)
                else:
                    pass
            else:
                pass
        MySQL.insert_distance_school_house(tuple_list)
    print("Finished")


if __name__ == "__main__":
    start = time.perf_counter()
    calculate_distance()
    end = time.perf_counter()
    print(end-start)


