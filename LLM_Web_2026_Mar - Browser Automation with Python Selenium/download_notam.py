import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

# နောက်ဆုံး pageမှာ next page ဆက်မလုပ်အောင်
# page တိုင်းရဲ့ ပထမ row ကို အမြဲ မှတ်ထားပြီး အဲ့ row က နောက် page ရဲ့ ပထမ row လည်းဖြစ်နေတယ်ဆိုရင်
# နောက် page ကို ဆက်မသွားပဲ while loop ရပ်မှာ ဖြစ်ပါတယ်။


def go_next_page(driver, first_before):
    driver.find_element(
        By.CSS_SELECTOR, 'td[onmousedown*="PagerNext"]'
    ).click()
    time.sleep(2)

    rows_after = driver.find_elements(By.CLASS_NAME, "GMDataRow")
    first_after = rows_after[0].text.strip()

    if first_before == first_after:
        print("Reached last page")
        return False

    return True


driver = webdriver.Chrome()
driver.get("https://aim.koca.go.kr/xNotam/index.do?type=search2&language=en_US#")
time.sleep(3)

file = open("notam_data.csv", mode="w", newline="", encoding="utf-8")
writer = csv.writer(file)
writer.writerow(["timestamp", "notam_text"])

page = 1

while True:
    print(f"\n📄 Page {page}")

    rows = driver.find_elements(By.CLASS_NAME, "GMDataRow")
    if not rows:
        print("No rows found")
        break

    # save first row text of current page for next-page comparison
    first_before = rows[0].text.strip()

    for i, row in enumerate(rows[:2]):
        print(f"\nClicking row {i+1}...")

        row.click()
        time.sleep(2)

        popup = driver.find_element(By.ID, "notamDetailBody")
        all_text = popup.text
        text = all_text.split("항목")[0].strip()
        print(text)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, text])
        file.flush()

        close_btn = driver.find_element(By.CLASS_NAME, "close")
        close_btn.click()
        time.sleep(2)

    if not go_next_page(driver, first_before):
        break

    page += 1

file.close()
driver.quit()
