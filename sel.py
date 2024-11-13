import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
# url = "http://localhost/phpmyadmin/index.php?route=/sql&pos=0&db=apt_delivery_evg&table=meals"
url = "http://127.0.0.1:8080/openserver/phpmyadmin/index.php?route=/sql&db=apt_delivery_evg&table=meals"

driver.get(url)
#
input_username = driver.find_element(By.ID, "input_username")
# input_password = driver.find_element(By.ID, "input_password")
input_go = driver.find_element(By.ID, "input_go")
input_username.send_keys("root")
# input_password.send_keys('123')
input_go.click()
time.sleep(1)
table = driver.find_element(By.CSS_SELECTOR, 'div.table-responsive-md > div > table')  # Локация таблицы по её идентификатору
# print(table.get_attribute('innerHTML'))

rows = table.find_elements(By.TAG_NAME, 'tr')  # Нахождение всех строк в таблице
for row in rows:
    cols = row.find_elements(By.CSS_SELECTOR, 'td:nth-child(7) > span, td:nth-child(8) > span, td:nth-child(9) > span, td:nth-child(11) > span')  # Нахождение всех столбцов в каждой строке
    for col in cols:
        print(col.get_attribute('innerHTML'))
    print()
time.sleep(10)
# driver.quit()