from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time

from wsproto.handshake import client_extensions_handshake

s = Service("C:/Users/avipy/Desktop/chromedriver.exe")

driver = webdriver.Chrome(service = s)

driver.get("https://www.smartprix.com/laptops/exclude_out_of_stock-exclude_upcoming-stock?sort=date&asc=0")
time.sleep(2)

old_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.find_element(by=By.XPATH, value='//*[@id="app"]/main/div[1]/div[2]/div[3]').click()
    time.sleep(1)
    new_height = driver.execute_script("return document.body.scrollHeight")
    print(old_height)
    print(new_height)
    if old_height == new_height:
        break
    old_height = new_height
html = driver.page_source
with open("../scraped/smartprix_laptops.html", "w",encoding='utf-8') as f:
    f.write(html)