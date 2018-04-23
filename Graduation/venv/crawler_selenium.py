from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import selenium.webdriver.support.ui as UI


def ajax_complete(dv):
    try:
        return 0 == dv.execute_script("return jQuery.active")
    except WebDriverException:
        pass


path = "C:/Users/M/Desktop/chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get('http://www.coupang.com/vp/products/27613130?itemId=109846121&vendorItemId=3213757282')

elem = driver.find_element_by_name('review')

review = []
while len(review) is 0:
    elem.click()
    review = driver.find_elements_by_class_name("sdp-review__article__page__num")
    driver.implicitly_wait(3)

review = driver.find_elements_by_xpath("//button[@data-page]")

wait = UI.WebDriverWait(driver, 10)

last_page = driver.find_element_by_xpath("//div[@data-end]").get_attribute("data-end")

temp = driver.find_element_by_class_name("sdp-review__average__total-star__info-count").text.split(",")

temp2 = temp[0] + temp[1]

total_page = int(int(temp2) / 50)

temp = driver.find_element_by_class_name("sdp-review__article__page")
data_start = int(temp.get_attribute("data-start"))
data_end = int(temp.get_attribute("data-end"))

for k in range(1, total_page):
    for i in range(data_start, data_end):
        next_page = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-page=' + str(i) + ']')))
        next_page.click()
        WebDriverWait(driver, 10).until(ajax_complete, "Timeout waiting for page to load")
        # 여기 부터 크롤링

    next_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sdp-review__article__page__next')))
    next_btn.click()
    WebDriverWait(driver, 10).until(ajax_complete, "Timeout waiting for page to load")

    temp = driver.find_element_by_class_name("sdp-review__article__page")
    data_start = int(temp.get_attribute("data-start")) + 1
    data_end = int(temp.get_attribute("data-end"))




