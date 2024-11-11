import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
url = "http://localhost/phpmyadmin/index.php?route=/sql&pos=0&db=apt_delivery_evg&table=meals"

driver.get(url)
#
input_username = driver.find_element(By.ID, "input_username")
input_password = driver.find_element(By.ID, "input_password")
input_go = driver.find_element(By.ID, "input_go")
input_username.send_keys("root")
input_password.send_keys('123')
input_go.click()
time.sleep(1)
table = driver.find_element(By.CSS_SELECTOR, '#resultsForm_1478223647')  # Локация таблицы по её идентификатору
print(table.get_attribute('innerHTML'))
# rows = table.find_elements(By.TAG_NAME, 'tr')  # Нахождение всех строк в таблице
# for row in rows:
#     cols = row.find_elements(By.CSS_SELECTOR, 'td')  # Нахождение всех столбцов в каждой строке
#     for col in cols:
#         print(col.get_attribute('innerHTML'))
time.sleep(10)
driver.quit()