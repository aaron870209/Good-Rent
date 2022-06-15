from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import threading

Taipei = "eJyrVkrOLKlUsopWMlCK1VFKySwuyEkE8pVyMotLlHSU8pOyMvNSQPJBIPni1MSi5AwQF6wNKFJanJqcn5IKEjIHqrcAYksgNjQAEsZKsbUArxsbyQ"
New_Taipei = "eJyrVkrOLKlUsopWMlKK1VFKySwuyEkE8pVyMotLlHSU8pOyMvNSQPJBIPni1MSi5AwQF6wNKFJanJqcn5IKEjIHqrcAYksgNjQAEsZKsbUAr8kbyw"


def crawler(region):
    driver = webdriver.Chrome()
    driver.get(f"https://www.rakuya.com.tw/search/rent_search/index?con={region}&upd=1")
    total_pages = driver.find_element(By.CLASS_NAME,"pages").text
    last_page = int(total_pages.split(' ')[3])
    print("last_page=",last_page)
    price = []
    title = []
    item_detail = []
    address = []
    img = []
    for paging in range(1,last_page+1):
        try:
            product_list = WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME,"obj-item.clearfix"))
            )
            price_1 = [x.find_element(By.CLASS_NAME,"obj-price").find_element(By.TAG_NAME,"span").text for x in product_list]
            print("price=", price_1)
            price.extend(price_1)
            title_1 = [x.find_element(By.CLASS_NAME,"obj-title").find_element(By.TAG_NAME,"a").text for x in product_list]
            print("title=",title_1)
            title.extend(title_1)
            item_detail_1 = [x.find_element(By.CLASS_NAME,"obj-data.clearfix").find_element(By.CLASS_NAME,"clearfix").text for x in product_list]
            print("detail=",item_detail_1)
            item_detail.extend(item_detail_1)
            address_1 = [x.find_element(By.CLASS_NAME,"obj-title").find_element(By.TAG_NAME,"p").text for x in product_list]
            print("address=",address_1)
            address.extend(address_1)
            img_1 = [re.search(r'https[a-z:\/.0-9_?]+',x.find_element(By.TAG_NAME,"a").get_attribute("style")).group(0) for x in product_list]
            print("img=",img_1)
            img.extend(img_1)
            if paging < 5:
                driver.find_element(By.XPATH, f"/html/body/div[8]/div/div[1]/nav/ul/li[{paging+2}]/a").click()
            elif paging > (last_page-3) and paging <= last_page:
                driver.find_element(By.XPATH, f"/html/body/div[8]/div/div[1]/nav/ul/li[{9-(last_page-paging)}]/a").click()
            elif paging <= last_page:
                driver.find_element(By.XPATH, f"/html/body/div[8]/div/div[1]/nav/ul/li[{6}]/a").click()
            else:
                driver.close()
        except:
            # for i in range(10):
            driver.refresh()
            # time.sleep(5)
            product_list = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "obj-item.clearfix"))
            )
            price_1 = [x.find_element(By.CLASS_NAME, "obj-price").find_element(By.TAG_NAME, "span").text for x in
                     product_list]
            print("price=", price_1)
            price.extend(price_1)
            title_1 = [x.find_element(By.CLASS_NAME, "obj-title").find_element(By.TAG_NAME, "a").text for x in
                     product_list]
            print("title=", title_1)
            title.extend(title_1)
            item_detail_1 = [
                x.find_element(By.CLASS_NAME, "obj-data.clearfix").find_element(By.CLASS_NAME, "clearfix").text for x in
                product_list]
            print("detail=", item_detail_1)
            item_detail.extend(item_detail_1)
            address_1 = [x.find_element(By.CLASS_NAME, "obj-title").find_element(By.TAG_NAME, "p").text for x in
                       product_list]
            print("address=", address_1)
            address.extend(address_1)
            img_1 = [re.search(r'https[a-z:\/.0-9_?]+', x.find_element(By.TAG_NAME, "a").get_attribute("style")).group(0)
                   for x in product_list]
            print("img=", img_1)
            img.extend(img_1)
            if paging < 5:
                driver.find_element(By.XPATH, f"/html/body/div[8]/div/div[1]/nav/ul/li[{paging + 2}]/a").click()
            elif paging > (last_page - 3) and paging <= last_page:
                driver.find_element(By.XPATH,
                                    f"/html/body/div[8]/div/div[1]/nav/ul/li[{9 - (last_page - paging)}]/a").click()
            elif paging <= last_page:
                driver.find_element(By.XPATH, f"/html/body/div[8]/div/div[1]/nav/ul/li[{6}]/a").click()
            else:
                driver.close()


t1 = threading.Thread(target=crawler, args=(Taipei,))
t2 = threading.Thread(target=crawler, args=(New_Taipei,))
t1.start()
t2.start()
t1.join()
t2.join()