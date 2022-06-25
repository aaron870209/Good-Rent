from dotenv import load_dotenv
from pymysqlpool.pool import Pool
import os
load_dotenv()


pool = Pool(host=os.getenv("host"), user=os.getenv("user"), password=os.getenv("password"), db=os.getenv("database"),
            charset='utf8mb4')
pool.init()
connection = pool.get_conn()
cursor = connection.cursor()


def insert_house_data_to_SQL(dict):
    type_dict = {"整層住家":1,"獨立套房":2,"分租套房":3,"雅房":4}
    city_dict = {"臺北市":1,"新北市":2}
    type_id = type_dict[dict["type"]]
    city_id = city_dict[dict["city"]]
    cursor.execute(
        "INSERT INTO `house` (`title`,`price`,`address`,`img`,`city_id`,`size`,`floor`,`type_id`,`key`) VALUEs "
        "(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (dict["title"],dict["price"],dict["address"],dict["img"],city_id,dict["size"],dict["floor"],
         type_id,dict["key"])
    )
    connection.commit()


def insert_truck_spot_to_SQL(dict):
    cursor.execute(
        "INSERT INTO `truck_spot` (`address`,`arrive_time`,`longitude`,`latitude`,`city_id`) VALUEs"
        "(%s,%s,%s,%s,%s)",
        (dict["address"],dict["arrive_time"],dict["longitude"],dict["latitude"],dict["city_id"])
    )
    connection.commit()


def update_house_log_lat(dict):
    cursor.execute(
        "UPDATE house SET longitude= %s,latitude=%s WHERE house_id = %s", (dict["log"], dict["lat"],dict["id"])
    )
    connection.commit()


def get_house_id():
    cursor.execute(
        "SELECT house_id,address,city_id FROM house WHERE longitude IS NULL"
    )
    # cursor.execute(
    #     "SELECT house_id,address,city_id FROM house WHERE house_id > 3934"
    # )
    house_list = cursor.fetchall()
    return house_list


def get_all_info_from_house(paging):
    cursor.execute(
        f"SELECT * FROM house INNER JOIN city ON house.city_id = city.city_id INNER JOIN type ON house.type_id = type.type_id LIMIT {int(paging)*15},15"
    )
    data_list = cursor.fetchall()
    return data_list


def get_house_detail_by_id(id):
    cursor.execute(
        "SELECT * FROM `house` INNER JOIN `city` ON house.city_id = city.city_id INNER JOIN type ON house.type_id = type.type_id WHERE `house_id` =%s",(id)
    )
    detail = cursor.fetchone()
    return detail


def search_house(tag):
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
    cursor.execute(
        "SELECT * FROM `house` INNER JOIN `city` ON house.city_id = city.city_id INNER JOIN type ON house.type_id = type.type_id"
        f" WHERE 1=1{region}{type}{rent}"
    )
    data = cursor.fetchall()
    return data