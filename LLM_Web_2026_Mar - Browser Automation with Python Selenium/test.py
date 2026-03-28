from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

driver.get("https://www.youtube.com")
time.sleep(3)

search_box = driver.find_element(By.NAME, "search_query")
search_box.send_keys("LaytLarMal Python")
time.sleep(3)

search_box.submit()
time.sleep(3)

driver.quit()
