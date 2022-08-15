from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import threading
from webdriver_manager.chrome import ChromeDriverManager
from mongo import mongo
import os
from dotenv import load_dotenv
load_dotenv()


def set_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.binary_location = os.getenv('options_location')
    driver = webdriver.Chrome(ChromeDriverManager(version="104.0.5112.20").install(), chrome_options=chrome_options)
    return driver


def get_total_page(driver):
    total_house = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "switch-amount"))
    ).find_element(By.TAG_NAME, "span")
    total_house_to_string = total_house.text
    total_house = int(total_house_to_string.replace(",", ""))
    last_page = int(total_house / 30)
    return total_house,last_page


def scroll_down(driver):
    import time
    for i in range(1, 18):
        driver.execute_script(f"window.scrollTo(0,500*{i})")
        time.sleep(0.5)


def find_element(position,class_name):
    return position.find_elements(By.CLASS_NAME, class_name)


def get_detail_info(driver,dict):
    position = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "switch-list-content"))
    )
    tag_list = find_element(position, "item-tags")
    price_list = find_element(position, "item-price-text")
    url_list = find_element(position, "vue-list-rent-item")
    title_list = find_element(position, "item-title")
    item_detail_list = find_element(position, "item-style")
    address_list = find_element(position, "item-area")
    scroll_down(driver)
    img_position = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "list-container-content"))
    )
    img_crawler_list = find_element(img_position, "carousel-list")
    price_1 = [x.text for x in price_list]
    tag_1 = [x.text for x in tag_list]
    url_1 = [x.find_element(By.TAG_NAME, "a").get_attribute("href") for x in url_list]
    title_1 = [x.text for x in title_list]
    item_detail_1 = [x.text for x in item_detail_list]
    address_1 = [x.find_element(By.TAG_NAME, "span").text.replace("-", "") for x in address_list]
    img_1 = [x.find_element(By.TAG_NAME, "img").get_attribute("src") for x in img_crawler_list]
    dict["price"].extend(price_1)
    dict["tag"].extend(tag_1)
    dict["url"].extend(url_1)
    dict["title"].extend(title_1)
    dict["item_detail"].extend(item_detail_1)
    dict["address"].extend(address_1)
    dict["img"].extend(img_1)
    return dict


def crawler(region):
    from datetime import date
    import time
    try:
        driver = set_driver()
        driver.get(f"https://rent.591.com.tw/?region={region}")
    except:
        print("File is busy")
        driver = set_driver()
        driver.get(f"https://rent.591.com.tw/?region={region}")
    total_house, last_page = get_total_page(driver)
    dict = {"title": [], "price": [], "item_detail": [], "address": [], "img": [], "source": "591",
            "region": None
        , "tag": [], "url": []}
    for paging in range(1, last_page+1):
        try:
            print(paging)
            dict = get_detail_info(driver,dict)
            if paging < last_page:
                driver.find_element(By.CLASS_NAME, 'pageNext').click()
            else:
                driver.quit()
        except:
            for x in range(10):
                print("error page on=", paging)
                driver.refresh()
                time.sleep(1)
                try:
                    dict = get_detail_info(driver,dict)
                    break
                except:
                    pass
                time.sleep(3)
            if paging < last_page:
                driver.find_element(By.CLASS_NAME, 'pageNext').click()
            else:
                driver.quit()
    if region == 1:
        dict["region"] = "臺北市"
    else:
        dict["region"] = "新北市"
    time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    today = date.today()
    dict_to_mongo = {"data":dict,"create_time":time,"create_date":str(today)}
    mongo.insert_data_to_mongo(dict_to_mongo)


t1 = threading.Thread(target=crawler, args=(1, ))
t2 = threading.Thread(target=crawler, args=(3, ))
t1.start()
t2.start()
t1.join()
t2.join()
