from dotenv import load_dotenv
from pymysqlpool.pool import Pool
import os
load_dotenv()


pool = Pool(host=os.getenv("host"), user=os.getenv("user"), password=os.getenv("password"), db=os.getenv("database"),
            charset='utf8mb4')
pool.init()
connection = pool.get_conn()
cursor = connection.cursor()


def insert_data_to_SQL(dict):
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


