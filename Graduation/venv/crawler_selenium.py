from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import selenium.webdriver.support.ui as UI
from selenium.common.exceptions import WebDriverException
import sync_ajax
import social_crawling

OUTPUT_FILE = "../output_file/output.txt"                                                       # 결과 파일
PATH = "../lib/chromedriver.exe"                                                                # path 지정 = 사용자 마다 경로 다르니까 그냥 lib directory에 selenium chromedriver 추가함
URL = 'http://www.coupang.com/vp/products/27613130?itemId=109846121&vendorItemId=3213757282'    # url 사용하기 위한 변수
result_text = ''

driver = webdriver.Chrome(PATH)
driver.get(URL)

# 리뷰 컨테이너 클릭
click_review = driver.find_element_by_name('review')

review = []
while len(review) is 0:
    click_review.click()
    review = driver.find_elements_by_class_name("sdp-review__article__page__num")
    driver.implicitly_wait(3)

review = driver.find_elements_by_xpath("//button[@data-page]")
wait = UI.WebDriverWait(driver, 10)
last_page = driver.find_element_by_xpath("//div[@data-end]").get_attribute("data-end")

# 전체 페이지 가져오기 - 숫자가 ,로 구분되어있음 (그러면 숫자가 , 없다면? split 무시되는가...?)
html_total_review_amount = driver.find_element_by_class_name("sdp-review__average__total-star__info-count").text.split(",")
total_review_amount = html_total_review_amount[0] + html_total_review_amount[1]
total_page = int(int(total_review_amount) / 50)

html_total_review_amount = driver.find_element_by_class_name("sdp-review__article__page")
data_start = int(html_total_review_amount.get_attribute("data-start"))
data_end = int(html_total_review_amount.get_attribute("data-end"))

for k in range(1, total_page):
    # 한 펭
    for i in range(data_start, data_end):
        next_page = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-page=' + str(i) + ']')))
        next_page.click()
        WebDriverWait(driver, 10).until(sync_ajax.ajax_complete, "Timeout waiting for page to load")
        # crawling
        html = driver.page_source
        notice = social_crawling.crawling_coupang_page(html)
        driver.implicitly_wait(5)
        result_text = str(notice[0]) +"\n" + str(notice[1]) +"\n"+ str(notice[2]) +"\n"+ str(notice[3]) +"\n"+ str(notice[4])+ "\n"
        # file open and write result_text
        open_result_file = open(OUTPUT_FILE, 'a', encoding='UTF-8', newline='')
        open_result_file.write(result_text)
        open_result_file.close()

    next_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sdp-review__article__page__next')))
    next_btn.click()
    WebDriverWait(driver, 10).until(sync_ajax.ajax_complete, "Timeout waiting for page to load")

    html_total_review_amount = driver.find_element_by_class_name("sdp-review__article__page")
    data_start = int(html_total_review_amount.get_attribute("data-start")) + 1
    data_end = int(html_total_review_amount.get_attribute("data-end"))
