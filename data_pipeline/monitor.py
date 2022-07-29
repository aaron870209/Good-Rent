from mongo import mongo
from datetime import date
from MySQL import MySQL
import os

today = date.today()


for x in mongo.get_data_from_mongo(str(today)):
    date_now = x["create_date"]
    print(date)
    count = len(x["data"]["title"])
    resource = x["data"]["source"]
    city = x["data"]["region"]
    if resource == "591" and city == "臺北市":
        count1 = count
        column = "mongo_data_count_591_Taipei"
        MySQL.monitor_data(column,count1,date_now)
    elif resource == "591" and city == "新北市":
        count2 = count
        column = "mongo_data_count_591_NewTaipei"
        MySQL.monitor_data(column, count2, date_now)
    elif resource == "樂屋網" and city == "臺北市":
        count3 = count
        column = "mongo_data_count_lewu_Taipei"
        MySQL.monitor_data(column, count3, date_now)
    elif resource == "樂屋網" and city == "新北市":
        count4 = count
        column = "mongo_data_count_lewu_NewTaipei"
        MySQL.monitor_data(column, count4, date_now)
os._exit(0)




