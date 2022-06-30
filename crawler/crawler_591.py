from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import threading
from webdriver_manager.chrome import ChromeDriverManager
from mongo import mongo


def crawler(region):
    from datetime import date
    import time
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
    driver.get(f"https://rent.591.com.tw/?region={region}")
    total_house = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "switch-amount"))
    ).find_element(By.TAG_NAME, "span")
    total_house_to_string = total_house.text
    total_house = int(total_house_to_string.replace(",", ""))
    last_page = int(total_house / 30)
    price = []
    title = []
    item_detail = []
    address = []
    img = []
    tag = []
    for i in range(1, last_page+1):
        try:
            price_list = WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "item-price-text"))
            )
            tag_list = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "item-tags"))
            )
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
            price_1 = [x.text for x in price_list]
            price.extend(price_1)
            tag_1 = [x.text for x in tag_list]
            tag.extend(tag_1)
            title_1 = [x.text for x in title_list]
            title.extend(title_1)
            item_detail_1 = [x.text for x in item_detail_list]
            item_detail.extend(item_detail_1)
            address_1 = [x.find_element(By.TAG_NAME,"span").text.replace("-","") for x in address_list]
            address.extend(address_1)
            img_1 = [x.find_element(By.TAG_NAME,"img").get_attribute("src") for x in img_crawler_list]
            img.extend(img_1)
            if i < last_page:
                driver.find_element(By.CLASS_NAME,'pageNext').click()
            else:
                driver.close()
        except:
            print(i)
            for x in range(3):
                driver.refresh()
                time.sleep(3)
            price_list = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "item-price-text"))
            )
            tag_list = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "item-tags")))
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
            tag_1 = [x.text for x in tag_list]
            tag.extend(tag_1)
            item_detail_1 = [x.text for x in item_detail_list]
            item_detail.extend(item_detail_1)
            address_1 = [x.find_element(By.TAG_NAME, "span").text.replace("-","") for x in address_list]
            address.extend(address_1)
            img_1 = [x.find_element(By.TAG_NAME, "img").get_attribute("src") for x in img_crawler_list]
            img.extend(img_1)
            if i < last_page:
                driver.find_element(By.CLASS_NAME, 'pageNext').click()
            else:
                driver.close()
    if region == 1:
        city="臺北市"
    else:
        city = "新北市"
    dict = {"title":title,"price":price,"item_detail":item_detail,"address":address,"img":img,"source":"591","region":city}
    time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    today = date.today()
    dict_to_mongo = {"data":dict,"create_time":time,"create_date":str(today)}
    mongo.insert_data_to_mongo(dict_to_mongo)


# def do_sth(driver, class_name):
#     total_house = WebDriverWait(driver,10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "switch-amount"))
#     ).find_element(By.TAG_NAME, "span")
#     return total_house


t1 = threading.Thread(target=crawler, args=(1, ))
t2 = threading.Thread(target=crawler, args=(3, ))
t1.start()
t2.start()
t1.join()
t2.join()