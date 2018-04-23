from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import selenium.webdriver.support.ui as UI

OUTPUT_FILE = "output.txt"

def ajax_complete(dv):
    try:
        return 0 == dv.execute_script("return jQuery.active")
    except WebDriverException:
        pass

# path 지정 = 사용자 마다 경로 다르니까 그냥 lib directory에 selenium chromedriver 추가함
path = "../lib/chromedriver.exe"
# url 사용하기 위한 변수
url = 'http://www.coupang.com/vp/products/27613130?itemId=109846121&vendorItemId=3213757282'
driver = webdriver.Chrome(path)
driver.get(url)

# 리뷰 컨테이너 클릭
elem = driver.find_element_by_name('review')

review = []
while len(review) is 0:
    elem.click()
    review = driver.find_elements_by_class_name("sdp-review__article__page__num")
    driver.implicitly_wait(3)

review = driver.find_elements_by_xpath("//button[@data-page]")
wait = UI.WebDriverWait(driver, 10)
last_page = driver.find_element_by_xpath("//div[@data-end]").get_attribute("data-end")

# 전체 페이지 가져오기
temp = driver.find_element_by_class_name("sdp-review__average__total-star__info-count").text.split(",")
temp2 = temp[0] + temp[1]

total_page = int(int(temp2) / 50)

temp = driver.find_element_by_class_name("sdp-review__article__page")
data_start = int(temp.get_attribute("data-start"))
data_end = int(temp.get_attribute("data-end"))

result_text = ''

for k in range(1, total_page):
    for i in range(data_start, data_end):
        next_page = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-page=' + str(i) + ']')))
        next_page.click()
        WebDriverWait(driver, 10).until(ajax_complete, "Timeout waiting for page to load")
        # 여기 부터 크롤링
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        notice = soup.find_all('div', {"class": "sdp-review__article__list__review__content js_reviewArticleContent"})
        driver.implicitly_wait(5)
        result_text = str(notice[0]) +"\n" + str(notice[1]) +"\n"+ str(notice[2]) +"\n"+ str(notice[3]) +"\n"+ str(notice[4])+ "\n"
        #print(str(notice[0]) + str(notice[1])+ str(notice[2]) + str(notice[3])+ str(notice[4]))
        open_result_file = open(OUTPUT_FILE, 'a', encoding='UTF-8', newline='')
        open_result_file.write(result_text)
        open_result_file.close()


    next_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sdp-review__article__page__next')))
    next_btn.click()
    WebDriverWait(driver, 10).until(ajax_complete, "Timeout waiting for page to load")

    temp = driver.find_element_by_class_name("sdp-review__article__page")
    data_start = int(temp.get_attribute("data-start")) + 1
    data_end = int(temp.get_attribute("data-end"))



# 파일에 text 쓰기
# open_result_file = open(OUTPUT_FILE,'w', encoding='UTF-8', newline='')
# open_result_file.write(result_text)
# open_result_file.close()