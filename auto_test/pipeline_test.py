from unittest.mock import patch
from data_pipeline import data_pipeline
from datetime import date


@patch('MySQL.MySQL.insert_house_data_to_SQL')
@patch('mongo.mongo.get_data_from_mongo')
def test_591(some_func, some_func2):
    today = str(date.today())
    some_func.return_value = [{"_id":15065423,"create_time":"2022-07-11 11:46:39","create_date":"2022-07-11",
                               "data":{"title":["金城商圈肯德基對面溫馨精緻幽靜 優選好屋"],
                                       "price":["9,500元/月"],"item_detail":["分租套房 8坪 5F/5F"],
                                       "address":["土城區延吉街296巷7弄4號"],
                                       "img":["https://img1.591.com.tw/house/2018/05/04/152536921152269109.jpg!510x40…"],
                                       "source":"591","region":"新北市",
                                       "tag":["屋主直租 新上架 拎包入住 近商圈 隨時可遷入 可養寵物"],
                                       "url":["https://rent.591.com.tw/rent-detail-12895076.html"]}}]
    some_func2.return_value = 0
    dict = data_pipeline.data_cleaning()
    assert dict == {"title": "金城商圈肯德基對面溫馨精緻幽靜 優選好屋","price":9500,"address":"土城區延吉街296巷7弄4號",
                    "img":"https://img1.591.com.tw/house/2018/05/04/152536921152269109.jpg!510x40…",
                             "type":"分租套房","size":"8坪","floor":"5","key":"土城區延吉街296巷7弄4號分租套房8坪5","city":"新北市"
        ,"tag":"屋主直租 新上架 拎包入住 近商圈 隨時可遷入 可養寵物","url":"https://rent.591.com.tw/rent-detail-12895076.html",
                    "date":today}


@patch('MySQL.MySQL.insert_house_data_to_SQL')
@patch('mongo.mongo.get_data_from_mongo')
def test_591_floor(some_func, some_func2):
    today = str(date.today())
    some_func.return_value = [{"_id":15065423,"create_time":"2022-07-11 11:46:39","create_date":"2022-07-11",
                               "data":{"title":["⭐大坪林公寓3樓，裝璜新"],
                                       "price":["10,500元/月"],"item_detail":["獨立套房 樓中樓 9坪 6F/12F"],
                                       "address":["土城區延吉街296巷7弄4號"],
                                       "img":["https://img1.591.com.tw/house/2018/05/04/152536921152269109.jpg!510x40…"],
                                       "source":"591","region":"新北市",
                                       "tag":["屋主直租 新上架 拎包入住 近商圈 隨時可遷入 可養寵物"],
                                       "url":["https://rent.591.com.tw/rent-detail-12895076.html"]}}]
    some_func2.return_value = 0
    dict = data_pipeline.data_cleaning()
    assert dict == {"title": "⭐大坪林公寓3樓，裝璜新","price":10500,"address":"土城區延吉街296巷7弄4號",
                    "img":"https://img1.591.com.tw/house/2018/05/04/152536921152269109.jpg!510x40…",
                             "type":"獨立套房","size":"9坪","floor":"6","key":"土城區延吉街296巷7弄4號獨立套房9坪6","city":"新北市"
        ,"tag":"屋主直租 新上架 拎包入住 近商圈 隨時可遷入 可養寵物","url":"https://rent.591.com.tw/rent-detail-12895076.html",
                    "date":today}


@patch('MySQL.MySQL.insert_house_data_to_SQL')
@patch('mongo.mongo.get_data_from_mongo')
def test_591_parking(some_func, some_func2):
    some_func.return_value = [{"_id":15065423,"create_time":"2022-07-11 11:46:39","create_date":"2022-07-11",
                               "data":{"title":["捷運松江南京站共構大樓室內車位"],
                                       "price":["4,200元/月"],"item_detail":["車位 機械式 5坪"],
                                       "address":["中山區南京東路二段108號"],
                                       "img":["https://img1.591.com.tw/house/2011/09/19/131644095344927800.jpg!510x40…"],
                                       "source":"591","region":"臺北市",
                                       "tag":["屋主直租 近捷運"],
                                       "url":["https://rent.591.com.tw/rent-detail-12746654.html"]}}]
    some_func2.return_value = 0
    dict = data_pipeline.data_cleaning()
    assert dict == None



@patch('MySQL.MySQL.insert_house_data_to_SQL')
@patch('mongo.mongo.get_data_from_mongo')
def test_lewu(some_func, some_func2):
    today = str(date.today())
    some_func.return_value = [{"_id":15065423,"create_time":"2022-07-11 11:46:39","create_date":"2022-07-11",
                               "data":{"title":["捷運新公館"],
                                       "price":["16.8萬"],"item_detail":["獨立套房/電梯大廈 -/11.8坪 9樓/24樓"],
                                       "address":["新北市新店區中興路三段"],
                                       "img":["https://static.rakuya.com.tw/r1/n099/87/7e/18891099_1_c.jpeg?165717451…"],
                                       "source":"樂屋網","region":"新北市",
                                       "url":["https://www.rakuya.com.tw/rent_item/info?ehid=0e5ac618891099e"]}}]
    some_func2.return_value = 0
    dict = data_pipeline.data_cleaning()
    assert dict == {"title": "捷運新公館","price":168000,"address":"新店區中興路三段",
                    "img":"https://static.rakuya.com.tw/r1/n099/87/7e/18891099_1_c.jpeg?165717451…",
                             "type":"獨立套房","size":"11.8坪","floor":"9","key":"新店區中興路三段獨立套房11.8坪9","city":"新北市"
        ,"tag":"電梯大廈","url":"https://www.rakuya.com.tw/rent_item/info?ehid=0e5ac618891099e",
                    "date":today}



