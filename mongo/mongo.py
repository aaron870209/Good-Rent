from pymongo import MongoClient
import pymysql.cursors
from pymysql import IntegrityError
import datetime
import re
import os
import time
from datetime import date
from dotenv import load_dotenv
load_dotenv()
client = MongoClient('localhost:27017',
                     username=os.getenv('mongo_user'),
                     password=os.getenv('mongo_password'),
                     # authSource='stylish_data_engineering',
                     # authMechanism='SCRAM-SHA-1'
                     )
db = client['crawler_data']
mycol = db["raw_data"]


def get_data_from_mongo(date):
    return mycol.find({"create_date": date})


def insert_data_to_mongo(dict):
    mycol.insert_one(dict)