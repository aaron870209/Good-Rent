from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv
import re
import threading
from mongo import mongo
load_dotenv()
Taipei = os.getenv('taipei_url')
New_Taipei = os.getenv('new_taipei_url')


def set_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.binary_location = os.getenv('options_location')
    driver = webdriver.Chrome(ChromeDriverManager(version="104.0.5112.20").install(), chrome_options=chrome_options)
    return driver


def get_last_page(driver):
    total_pages = driver.find_element(By.CLASS_NAME,"pages").text
    last_page = int(total_pages.split(' ')[3])
    return total_pages,last_page


def change_pages(driver,paging,last_page):
    if paging < 5:
        driver.find_element(By.XPATH, f"/html/body/div[8]/div/div[1]/nav/ul/li[{paging + 2}]/a").click()
    elif paging > (last_page - 3) and paging <= last_page:
        driver.find_element(By.XPATH, f"/html/body/div[8]/div/div[1]/nav/ul/li[{9 - (last_page - paging)}]/a").click()
    elif paging < last_page:
        driver.find_element(By.XPATH, f"/html/body/div[8]/div/div[1]/nav/ul/li[{6}]/a").click()
    else:
        driver.quit()


def get_detail_info(product_list,dict):
    price_1 = [x.find_element(By.CLASS_NAME, "obj-price").find_element(By.TAG_NAME, "span").text for x in product_list]
    dict["price"].extend(price_1)
    url_1 = [x.find_element(By.CLASS_NAME, "obj-title").find_element(By.TAG_NAME, "a").get_attribute("href") for
             x in product_list]
    dict["url"].extend(url_1)
    title_1 = [x.find_element(By.CLASS_NAME, "obj-title").find_element(By.TAG_NAME, "a").text for x in product_list]
    dict["title"].extend(title_1)
    item_detail_1 = []
    for i in product_list:
        detail_list = i.find_element(By.CLASS_NAME, "obj-data.clearfix").find_elements(By.CLASS_NAME,
                                                                                       "clearfix")
        detail = detail_list[0].text + "/" + detail_list[1].text
        item_detail_1.append(detail)
    dict["item_detail"].extend(item_detail_1)
    address_1 = [x.find_element(By.CLASS_NAME, "obj-title").find_element(By.TAG_NAME, "p").text for x in product_list]
    dict["address"].extend(address_1)
    img_1 = [re.search(r'https[a-z:\/.0-9_?]+', x.find_element(By.TAG_NAME, "a").get_attribute("style")).group(0) for x
             in product_list]
    dict["img"].extend(img_1)
    return dict


def crawler(region):
    from datetime import date
    import time
    driver = set_driver()
    driver.get(f"https://www.rakuya.com.tw/search/rent_search/index?con={region}&upd=1")
    total_pages, last_page = get_last_page(driver)
    dict = {"title":[],"price":[],"item_detail":[],"address":[],"img":[],"source":"樂屋網","region":None,"url":[]}
    for paging in range(1,3):
        try:
            product_list = WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME,"obj-item.clearfix"))
            )
            dict = get_detail_info(product_list,dict)
            change_pages(driver,paging,last_page)
        except:
            for i in range(20):
                print(paging)
                try:
                    product_list = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "obj-item.clearfix"))
                    )
                    break
                except:
                    driver.refresh()
                    time.sleep(3)
            dict = get_detail_info(product_list, dict)
            change_pages(driver,paging,last_page)
    if region == os.getenv('taipei_url'):
        dict["region"] = "臺北市"
    else:
        dict["region"] = "新北市"
    today = date.today()
    time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    dict_to_mongo = {"data":dict, "create_time":time, "create_date":str(today)}
    mongo.insert_data_to_mongo(dict_to_mongo)


t1 = threading.Thread(target=crawler, args=(Taipei,))
t2 = threading.Thread(target=crawler, args=(New_Taipei,))
t1.start()
t2.start()
t1.join()
t2.join()
print("Finished")