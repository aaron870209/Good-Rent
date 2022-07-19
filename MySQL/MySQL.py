from dotenv import load_dotenv
from pymysqlpool.pool import Pool
from datetime import date
import os
import datetime
load_dotenv()


pool = Pool(host=os.getenv("host"), user=os.getenv("user"), password=os.getenv("password"), db=os.getenv("database"),
            charset='utf8mb4')
pool.init()
connection = pool.get_conn()
cursor = connection.cursor()
today = date.today()
yesterday = today-datetime.timedelta(days=1)


def insert_house_data_to_SQL(dict):
    connection.ping(reconnect=True)
    type_dict = {"整層住家":1,"獨立套房":2,"分租套房":3,"雅房":4}
    city_dict = {"臺北市":1,"新北市":2}
    type_id = type_dict[dict["type"]]
    city_id = city_dict[dict["city"]]
    cursor.execute(
        "INSERT INTO `house` (`title`,`price`,`address`,`img`,`city_id`,`size`,`floor`,`type_id`,`key`,`url`,`tag`,`date`) VALUEs "
        "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE `url`=%s,`tag`=%s,`date`=%s,img=%s,title=%s",
        (dict["title"],dict["price"],dict["address"],dict["img"],city_id,dict["size"],dict["floor"],
         type_id,dict["key"],dict["url"],dict["tag"],dict["date"],dict["url"],dict["tag"],dict["date"],dict["img"],dict["title"])
    )
    connection.commit()


def insert_truck_spot_to_SQL(dict):
    connection.ping(reconnect=True)
    cursor.execute(
        "INSERT INTO `truck_spot` (`address`,`arrive_time`,`longitude`,`latitude`,`city_id`) VALUEs"
        "(%s,%s,%s,%s,%s)",
        (dict["address"],dict["arrive_time"],dict["longitude"],dict["latitude"],dict["city_id"])
    )
    connection.commit()


def update_house_log_lat(dict):
    connection.ping(reconnect=True)
    cursor.execute(
        "UPDATE house SET longitude= %s,latitude=%s WHERE house_id = %s", (dict["log"], dict["lat"],dict["id"])
    )
    connection.commit()


def get_house_id():
    connection.ping(reconnect=True)
    cursor.execute(
        "SELECT house_id,address,city_id FROM house WHERE longitude IS NULL"
    )
    # cursor.execute(
    #     "SELECT house_id,address,city_id FROM house WHERE house_id > 3934"
    # )
    house_list = cursor.fetchall()
    return house_list


def get_all_info_from_house(paging):
    connection.ping(reconnect=True)
    cursor.execute(
        f"SELECT count(*) FROM house INNER JOIN city ON house.city_id = city.city_id INNER JOIN type ON house.type_id = type.type_id WHERE url IS NOT NULL AND date='{str(yesterday)}'"
    )
    total = cursor.fetchone()
    connection.commit()
    cursor.execute(
        f"SELECT * FROM house INNER JOIN city ON house.city_id = city.city_id INNER JOIN type ON house.type_id = type.type_id WHERE url IS NOT NULL AND date='{str(yesterday)}' LIMIT {int(paging)*15},15"
    )
    data_list = cursor.fetchall()
    return data_list,total


def get_filter_info_from_house(paging, tag):
    connection.ping(reconnect=True)
    if tag == 1:
        cursor.execute(
            f"SELECT count(*) FROM house INNER JOIN city ON house.city_id = city.city_id INNER JOIN type ON house.type_id = type.type_id WHERE url IS NOT NULL and (floor < 4 OR tag like '%電梯%') and floor NOT LIKE '%頂樓加蓋%' and date='{str(yesterday)}'"
        )
        total = cursor.fetchone()
        connection.commit()
        cursor.execute(
            f"SELECT * FROM house INNER JOIN city ON house.city_id = city.city_id INNER JOIN type ON house.type_id = type.type_id WHERE url IS NOT NULL and (floor < 4 OR tag like '%電梯%') and floor NOT LIKE '%頂樓加蓋%' and date='{str(yesterday)}' LIMIT {int(paging)*15},15"
        )
        data_list = cursor.fetchall()
        return data_list,total
    elif tag == 2:
        cursor.execute(
            f"SELECT count(*) FROM house INNER JOIN city ON house.city_id = city.city_id INNER JOIN type ON house.type_id = type.type_id WHERE url IS NOT NULL and (house_type = '雅房' OR house_type = '分租套房') and date='{str(yesterday)}'"
        )
        total = cursor.fetchone()
        connection.commit()
        cursor.execute(
            f"SELECT * FROM house INNER JOIN city ON house.city_id = city.city_id INNER JOIN type ON house.type_id = type.type_id WHERE url IS NOT NULL and (house_type = '雅房' OR house_type = '分租套房') and date='{str(yesterday)}' LIMIT {int(paging)*15},15"
        )
        data_list = cursor.fetchall()
        return data_list,total
    elif tag == 3:
        cursor.execute(
            f"SELECT count(*) FROM house INNER JOIN city ON house.city_id = city.city_id INNER JOIN type ON house.type_id = type.type_id WHERE url IS NOT NULL and house_type='整層住家' and date='{str(yesterday)}'"
        )
        total = cursor.fetchone()
        connection.commit()
        cursor.execute(
            f"SELECT * FROM house INNER JOIN city ON house.city_id = city.city_id INNER JOIN type ON house.type_id = type.type_id WHERE url IS NOT NULL and house_type='整層住家' and date='{str(yesterday)}' LIMIT {int(paging)*15},15"
        )
        data_list = cursor.fetchall()
        return data_list,total


def get_house_detail_by_id(id):
    connection.ping(reconnect=True)
    cursor.execute(
        "SELECT * FROM `house` INNER JOIN `city` ON house.city_id = city.city_id INNER JOIN type ON house.type_id = type.type_id WHERE `house_id` =%s ",(id)
    )
    detail = cursor.fetchone()
    return detail


def search_house(tag,page):
    connection.ping(reconnect=True)
    taipei = tag["taipei"]
    print("taipei=",taipei)
    new_taipei = tag["new_taipei"]
    print("new_taipei=", new_taipei)
    region_list = taipei+new_taipei
    type_list = tag["type"]
    rent_list = tag["rent"]
    print(region_list)
    #地區搜尋
    if region_list != []:
        if len(region_list) == 1:
            region = f' AND (address LIKE "%{region_list[0]}%")'
        else:
            for count in range(len(region_list)):
                if count == 0:
                    region = f' AND (address LIKE "%{region_list[count]}%"'
                elif count == len(region_list) - 1:
                    region = region + f' OR address LIKE "%{region_list[count]}%")'
                else:
                    region = region + f' OR address LIKE "%{region_list[count]}%"'

    else:
        region = ''

    #類型搜尋
    if type_list != []:
        if len(type_list) == 1:
            type = f' AND (house_type = "{type_list[0]}")'
        else:
            for count in range(len(type_list)):
                if count == 0:
                    type = f' AND (house_type = "{type_list[count]}"'
                elif count == len(type_list)-1:
                    type = type + f' OR house_type = "{type_list[count]}")'
                else:
                    type = type + f' OR house_type = "{type_list[count]}"'

    else:
        type = ''
    #租金搜尋
    if rent_list != []:
        if rent_list[0] == "5000元以下":
            rent = ' AND price < 5000'
        elif rent_list[0] == "5000元~10000元":
            rent = ' AND price BETWEEN 5000 AND 10000'
        elif rent_list[0] == "10000元~15000元":
            rent = ' AND price BETWEEN 10000 AND 15000'
        elif rent_list[0] == "15000元~20000元":
            rent = ' AND price BETWEEN 15000 AND 20000'
        else:
            rent = ' AND price > 20000'
    else:
        rent = ''
    print("region=",region)
    print("type=",type)
    print("rent",rent)
    paging = page*15
    cursor.execute(
        "SELECT count(*) FROM `house` INNER JOIN `city` ON house.city_id = city.city_id INNER JOIN type ON house.type_id = type.type_id"
        f" WHERE 1=1{region}{type}{rent} and url IS NOT NULL and date='{str(yesterday)}'"
    )
    total = cursor.fetchone()
    connection.commit()
    cursor.execute(
        "SELECT * FROM `house` INNER JOIN `city` ON house.city_id = city.city_id INNER JOIN type ON house.type_id = type.type_id"
        f" WHERE 1=1{region}{type}{rent} and url IS NOT NULL and date='{str(yesterday)}' LIMIT {paging},15"
    )
    data = cursor.fetchall()
    return data,total


def get_house_lat_lon():
    today = date.today()
    connection.ping(reconnect=True)
    cursor.execute(
        "SELECT house_id,longitude,latitude,city_id from house WHERE date=%s AND `update` IS NULL",(str(today))
    )
    return cursor.fetchall()


def get_truck_lat_lon():
    connection.ping(reconnect=True)
    cursor.execute(
        "SELECT truck_spot_id, longitude,latitude,city_id FROM truck_spot"
    )
    return cursor.fetchall()


def get_school_lat_lon():
    connection.ping(reconnect=True)
    cursor.execute(
        "SELECT school_id, longitude,latitude,city_id FROM school"
    )
    return cursor.fetchall()


def insert_distance_truck_house(tuple_list):
    connection.ping(reconnect=True)
    stmt = "INSERT INTO house_truck_distance (house_id,truck_spot_id,distance) VALUES (%s,%s,%s)"
    cursor.executemany(stmt, tuple_list)
    connection.commit()


def insert_distance_school_house(tuple_list):
    connection.ping(reconnect=True)
    stmt = "INSERT INTO house_school_distance (house_id,school_id,distance) VALUES (%s,%s,%s)"
    cursor.executemany(stmt, tuple_list)
    connection.commit()


def get_truck_house_distance(house_id):
    connection.ping(reconnect=True)
    cursor.execute(
        "SELECT truck_spot_id FROM house_truck_distance WHERE house_id=%s ORDER BY distance LIMIT 0,3", (house_id)
    )
    return cursor.fetchall()


def get_school_house_distance(house_id):
    connection.ping(reconnect=True)
    cursor.execute(
        "SELECT school_id FROM house_school_distance WHERE house_id=%s ORDER BY distance LIMIT 0,3", (house_id)
    )
    return cursor.fetchall()


def get_truck_lon_lat_by_id(spot_id):
    connection.ping(reconnect=True)
    cursor.execute(
        "SELECT longitude,latitude FROM truck_spot WHERE truck_spot_id =%s",(spot_id)
    )
    return cursor.fetchone()


def insert_school_spot(list):
    connection.ping(reconnect=True)
    stmt = "INSERT INTO school (name,address,longitude,latitude,city_id) VALUES (%s,%s,%s,%s,%s)"
    cursor.executemany(stmt, list)
    connection.commit()


def get_school_lon_lat_by_id(spot_id):
    connection.ping(reconnect=True)
    cursor.execute(
        "SELECT longitude,latitude,name FROM school WHERE school_id =%s",(spot_id)
    )
    return cursor.fetchone()


def finish_update(id_list):
    connection.ping(reconnect=True)
    stmt = f"UPDATE house SET `update`=1 WHERE house_id IN {tuple(id_list)}"
    cursor.execute(stmt)
    connection.commit()


def add_new_data_count(total_list):
    count = len(total_list)
    connection.ping(reconnect=True)
    cursor.execute(
        "INSERT INTO monitor (`date`,new_data_count) VALUES (%s,%s)",(str(today),count)
    )
    connection.commit()


def login(email):
    cursor.execute(
        "SELECT `email`,`password` FROM `user` WHERE `email`=%s",(email)
    )
    user = cursor.fetchone()
    email = user["email"]
    password = user["password"]
    return email,password


def monitor_data(column,count,date):
    cursor.execute(
            f"INSERT INTO monitor (`date`,{column}) VALUES (%s,%s) ON DUPLICATE KEY UPDATE "
            f"{column}=%s", (date, count,count)
        )
    connection.commit()

def get_monitor_data():
    cursor.execute(
        "SELECT * FROM monitor ORDER BY `date` DESC limit 0,10"
    )
    return cursor.fetchall()