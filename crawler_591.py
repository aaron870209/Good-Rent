from fake_useragent import UserAgent
import requests
import pymysql.cursors
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from dotenv import load_dotenv
import threading

load_dotenv()
client = MongoClient('localhost:27017',
                     username=os.getenv('mongo_user'),
                     password=os.getenv('mongo_password'),
                     # authSource='stylish_data_engineering',
                     # authMechanism='SCRAM-SHA-1'
                     )
db = client['admin']
mycol = db["test_col"]


def crawler(region):
    start = time.perf_counter()
    driver = webdriver.Chrome()
    driver.get(f"https://rent.591.com.tw/?region={region}")
    # time.sleep(3)
    price_list = WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "item-price-text"))
    )
    total_house = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "switch-amount"))
    ).find_element(By.TAG_NAME, "span")
    title_list = WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME,"item-title"))
    )
    item_detail_list = WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME,"item-style"))
    )
    address_list = WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME,"item-area"))
    )
    for i in range(1,17):
        driver.execute_script(f"window.scrollTo(0,500*{i})")
        time.sleep(0.5)
    img_crawler_list = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "list-container-content"))
    ).find_elements(By.CLASS_NAME,"carousel-list")
    total_house_to_string = total_house.text
    total_house = int(total_house_to_string.replace(",", ""))
    price = [x.text for x in price_list]
    title = [x.text for x in title_list]
    item_detail = [x.text for x in item_detail_list]
    address = [x.find_element(By.TAG_NAME,"span").text for x in address_list]
    img = [x.find_element(By.TAG_NAME,"img").get_attribute("src") for x in img_crawler_list]
    page = int(total_house/30)
    print("Total=", total_house)
    print("price=", price)
    print("title=", title)
    print("detail=", item_detail)
    print("address=", address)
    print("img=",img)
    print(page)
    driver.close()
    for i in range(1, 5):
        first_row = i*30
        total_row = total_house
        driver = webdriver.Chrome()
        driver.get(f"https://rent.591.com.tw/?region={region}&firstRow={first_row}&totalRows={total_row}")
        price_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "item-price-text"))
        )
        title_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "item-title"))
        )
        item_detail_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "item-style"))
        )
        address_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "item-area"))
        )
        for i in range(1, 17):
            driver.execute_script(f"window.scrollTo(0,500*{i})")
            time.sleep(0.5)
        img_crawler_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "list-container-content"))
        ).find_elements(By.CLASS_NAME, "carousel-list")
        price_1 = [x.text for x in price_list]
        price.extend(price_1)
        title_1 = [x.text for x in title_list]
        title.extend(title_1)
        item_detail_1 = [x.text for x in item_detail_list]
        item_detail.extend(item_detail_1)
        address_1 = [x.text for x in address_list]
        address.extend(address_1)
        img_1 = [x.find_element(By.TAG_NAME, "img").get_attribute("src") for x in img_crawler_list]
        img.extend(img_1)
        driver.close()
    print("price=", price)
    print("title=", title)
    print("detail=", item_detail)
    print("address=", address)
    print("img=",img)
    end = time.perf_counter()
    print("time=",end-start)


t1 = threading.Thread(target=crawler ,args=(1,))
t2 = threading.Thread(target=crawler, args=(3,))
t1.start()
t2.start()
t1.join()
t2.join()