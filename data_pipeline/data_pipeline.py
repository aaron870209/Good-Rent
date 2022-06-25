from pymysql import IntegrityError
import time
from datetime import date
from mongo import mongo
from MySQL import MySQL


def data_cleaning():
    date_test = "2022-06-18"
    raw_data_list = mongo.get_data_from_mongo(date_test)
    for raw_data in raw_data_list:
        for length in range(len(raw_data["data"]["title"])):
            data = raw_data["data"]
            title = data["title"][length]
            detail = data["item_detail"][length]
            print("detail=", detail)
            if data["source"] == "591":
                type = detail.split(" ")[0]
                if type == "整層住家":
                    size = detail.split(" ")[2]
                    floor = detail.split(" ")[3].split("F")[0]
                else:
                    size = detail.split(" ")[1]
                    floor = detail.split(" ")[2].split("F")[0]
            else:
                type = detail.split("/")[0]
                size = detail.split("/")[2].split("\n")[0]
                floor = detail.split("/")[2].split("\n")[1].split("樓")[0]
            if type == "車位" or type == "其他":
                pass
            else:
                if "萬" in data["price"][length]:
                    price = int(float(data["price"][length].replace("萬", "").replace("元","").replace(",",''))*10000)
                else:
                    price = int(data["price"][length].replace("元",'').replace(",",'').replace("/月",""))
                print("type=", type)
                print("size=", size)
                print("floor=", floor)
                city = data["region"]
                print("city=",city)
                address = data["address"][length]
                print("address=",address)
                img = data["img"][length]
                print("img=",img)
                key = address+type+size+floor
                print("key=",key)
                data_dict = {"title": title,"price":price,"address":address,"img":img,
                             "type":type,"size":size,"floor":floor,"key":key,"city":city}
                try:
                    MySQL.insert_house_data_to_SQL(data_dict)
                except IntegrityError:
                    print(title,city,address)
                    pass


data_cleaning()