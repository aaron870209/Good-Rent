from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from MySQL import MySQL
import threading


def get_coordinate(addr, house_id):
    try:
        import time
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get("http://www.map.com.tw/")
        search = browser.find_element_by_id("searchWord")
        search.clear()
        search.send_keys(addr)
        browser.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click()
        # time.sleep(5)
        time.sleep(3)
        iframe = browser.find_element_by_class_name('winfoIframe')
        print(iframe)
        browser.switch_to.frame(iframe)
        # time.sleep(3)
        coor_btn = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]"))
                )
        # coor_btn = browser.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]")
        coor_btn.click()
        coor = browser.find_element_by_xpath("/html/body/form/div[5]/table/tbody/tr[2]/td")
        coor = coor.text.strip().split(" ")
        lat = coor[-1].split("：")[-1]
        log = coor[0].split("：")[-1]
        browser.quit()
        dict = {"log":log,"lat":lat,"id":house_id}
        MySQL.update_house_log_lat(dict)
    except:
        browser.refresh()
        search = browser.find_element_by_id("searchWord")
        search.clear()
        search.send_keys(addr)
        browser.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click()
        time.sleep(5)
        iframe = browser.find_element_by_class_name('winfoIframe')
        print(iframe.text)
        browser.switch_to.frame(iframe)
        time.sleep(3)
        coor_btn = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]"))
                )
        # coor_btn = browser.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]")
        coor_btn.click()
        coor = browser.find_element_by_xpath("/html/body/form/div[5]/table/tbody/tr[2]/td")
        coor = coor.text.strip().split(" ")
        lat = coor[-1].split("：")[-1]
        log = coor[0].split("：")[-1]
        browser.quit()
        dict = {"log":log,"lat":lat,"id":house_id}
        MySQL.update_house_log_lat(dict)


def get_data_from_DB():
    for house in MySQL.get_house_id():
        city_id = house["city_id"]
        if city_id == 1:
            city = "台北市"
        else:
            city = "新北市"
        house_id = house["house_id"]
        address = city + house["address"]
        get_coordinate(address,house_id)


if __name__ == "__main__":
    get_data_from_DB()
    print("Finished")