import time
from datetime import date
from mongo import mongo
from MySQL import MySQL
import os


def data_cleaning():
    today = str(date.today())
    raw_data_list = mongo.get_data_from_mongo(today)
    count=0
    for raw_data in raw_data_list:
        for length in range(len(raw_data["data"]["title"])):
            print(count)
            data = raw_data["data"]
            title = data["title"][length]
            detail = data["item_detail"][length]
            url = data["url"][length]
            if data["source"] == "591":
                tag = data["tag"][length]
                type = detail.split(" ")[0]
                if type == "整層住家":
                    size = detail.split(" ")[2]
                    floor = detail.split(" ")[3].split("F")[0]
                elif type == "車位" or type =="其他":
                    pass
                else:
                    size = detail.split(" ")[1]
                    if size == "樓中樓":
                        size = detail.split(" ")[2]
                        floor = detail.split(" ")[3].split("F")[0]
                    else:
                        floor = detail.split(" ")[2].split("F")[0]
            else:
                type = detail.split("/")[0]
                tag = detail.split("/")[1].split(" ")[0]
                size = detail.split("/")[2].split(" ")[0]
                floor = detail.split("/")[2].split(" ")[1].split("樓")[0]
            if type == "車位" or type == "其他":
                data_dict = None
            else:
                if "萬" in data["price"][length]:
                    price = int(float(data["price"][length].replace("萬", "").replace("元","").replace(",",''))*10000)
                else:
                    price = int(data["price"][length].replace("元",'').replace(",",'').replace("/月",""))
                city = data["region"]
                address = data["address"][length].replace("台北市","").replace("新北市","")
                img = data["img"][length]
                key = address+type+size+floor
                data_dict = {"title": title,"price":price,"address":address,"img":img,
                             "type":type,"size":size,"floor":floor,"key":key,"city":city,"tag":tag,"url":url,"date":today}
                MySQL.insert_house_data_to_SQL(data_dict)
                count += 1
    return data_dict


if __name__ == "__main__":
    start = time.perf_counter()
    data_cleaning()
    end = time.perf_counter()
    print(end-start)
    print("Finished")
    os._exit(0)