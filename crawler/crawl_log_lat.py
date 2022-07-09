from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from MySQL import MySQL
import threading
from geopy.geocoders import Nominatim
import random
import os
from geopy.extra.rate_limiter import RateLimiter
from dotenv import load_dotenv
load_dotenv()

def get_coordinate(addr, house_id):
    try:
        i = random.randint(3, 8)
        import time
        chrome_options = Options()
        ua = UserAgent().random
        # chrome_options.add_argument('--proxy-server=http://202.20.16.82:10152')
        chrome_options.add_argument('--headless')
        # chrome_options.add_argument("user-agent={}".format(ua))
        chrome_options.binary_location = os.getenv('options_location')
        browser = webdriver.Chrome(ChromeDriverManager(version="104.0.5112.20").install(), chrome_options=chrome_options)
        browser.get("http://www.map.com.tw/")
        time.sleep(i)
        search = browser.find_element(By.ID, "searchWord")
        search.clear()
        search.send_keys(addr)
        browser.find_element(By.XPATH, "/html/body/form/div[10]/div[2]/img[2]").click()
        # time.sleep(5)
        time.sleep(i)
        iframe = browser.find_element(By.CLASS_NAME, 'winfoIframe')
        browser.switch_to.frame(iframe)
        time.sleep(i)
        coor_btn = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]"))
        )
        # coor_btn = browser.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]")
        coor_btn.click()
        coor = browser.find_element(By.XPATH, "/html/body/form/div[5]/table/tbody/tr[2]/td")
        coor = coor.text.strip().split(" ")
        lat = coor[-1].split("：")[-1]
        log = coor[0].split("：")[-1]
        browser.quit()
        dict = {"log": log, "lat": lat, "id": house_id}
        MySQL.update_house_log_lat(dict)
        time.sleep(i)
    except:
        browser.quit()
        chrome_options = Options()
        ua = UserAgent().random
        chrome_options.add_argument('--headless')
        chrome_options.binary_location = os.getenv('options_location')
        browser = webdriver.Chrome(ChromeDriverManager(version="104.0.5112.20").install(), chrome_options=chrome_options)
        browser.get("http://www.map.com.tw/")
        time.sleep(3)
        search = browser.find_element(By.ID, "searchWord")
        search.clear()
        search.send_keys(addr)
        browser.find_element(By.XPATH, "/html/body/form/div[10]/div[2]/img[2]").click()
        time.sleep(5)
        iframe = browser.find_element(By.CLASS_NAME, 'winfoIframe')
        browser.switch_to.frame(iframe)
        time.sleep(3)
        coor_btn = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]"))
        )
        # coor_btn = browser.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]")
        coor_btn.click()
        coor = browser.find_element(By.XPATH, "/html/body/form/div[5]/table/tbody/tr[2]/td")
        coor = coor.text.strip().split(" ")
        lat = coor[-1].split("：")[-1]
        log = coor[0].split("：")[-1]
        browser.quit()
        dict = {"log": log, "lat": lat, "id": house_id}
        MySQL.update_house_log_lat(dict)


def change_address_to_latlon(address,house_id):
    geolocator = Nominatim(user_agent="GoodRent")
    try:
        location = RateLimiter(geolocator.geocode(address),min_delay_seconds=1)
        longitude = location.longitude
        latitude = location.latitude
        dict = {"log": longitude, "lat": latitude, "id": house_id}
        MySQL.update_house_log_lat(dict)
    except AttributeError:
        try:
            address1 = address.replace("台北市","").replace("新北市","")
            location = geolocator.geocode(address1)
            longitude = location.longitude
            latitude = location.latitude
            dict = {"log": longitude, "lat": latitude, "id": house_id}
            MySQL.update_house_log_lat(dict)
        except:
            get_coordinate(address, house_id)
    except:
        get_coordinate(address, house_id)

def get_data_from_DB():
    for house in MySQL.get_house_id():
        city_id = house["city_id"]
        if city_id == 1:
            city = "台北市"
        else:
            city = "新北市"
        house_id = house["house_id"]
        address = city + house["address"]
        print(house_id)
        change_address_to_latlon(address,house_id)


if __name__ == "__main__":
    get_data_from_DB()
    print("Finished")